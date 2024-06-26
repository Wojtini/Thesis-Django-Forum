from datetime import timedelta, datetime
from typing import List

from django.core.management.base import BaseCommand
from django.db.models import Sum
from django.utils import timezone

from Masquerade.settings import SAFE_CYCLES, MINIMUM_POPULARITY, MAX_FILESIZE_PER_THREAD_MB, MINIMUM_ALPHA_COEFFICENT, \
    MAXIMUM_ALPHA_COEFFICENT, ENTRY_POPULARITY_CALCULATORS, SAFE_MINUTES
from forum.models import Thread, Entry, Cycle, CycleThread, User, Category


class Command(BaseCommand):
    help = "Perform popularity step"

    def handle(self, *args, **options):
        self.log(self.style.SUCCESS(f"Creating new cycle"))
        new_cycle = Cycle()
        new_cycle.save()
        threads = Thread.objects.filter(created_date__lte=self.previous_date())
        self.log(f"Got {len(threads)} thread(s)")
        for thread in threads:
            self.process_thread(new_cycle, thread)
        self.clear_empty_categories()
        self.clear_empty_users()

    def log(self, msg):
        self.stdout.write(f"{datetime.now()}: {msg}")

    def clear_empty_categories(self):
        categories_to_delete = [
            category
            for category in Category.objects.filter(created_date__lte=self.previous_date())
            if category.threads_amount == 0
        ]
        for category in categories_to_delete:
            self.log(f"Deleting {category.name} empty category")
            category.delete()

    def clear_empty_users(self):
        users_to_clear = [
            user
            for user in User.objects.filter(created_at__lte=self.previous_date())
            if user.threads_amount + user.categories_amount + user.entries_amount == 0
        ]
        for user in users_to_clear:
            self.log(f"Deleting {user} inactive user")
            user.delete()

    def process_thread(self, cycle: Cycle, thread: Thread):
        self.log(f"Processing {thread}")
        new_popularity = self.calculate_popularity_from_new_entries(thread)
        if thread_cycles := CycleThread.objects.filter(thread=thread):
            cycles_amount = len(thread_cycles)
        else:
            cycles_amount = 0
        self.log(f"Thread in {cycles_amount} cycles")
        new_cycle_thread = CycleThread(cycle=cycle, thread=thread, popularity=0)
        if cycles_amount < SAFE_CYCLES:
            self.log(f"Setting new popularity for safe thread")
            new_cycle_thread.popularity = new_popularity
            new_cycle_thread.save()
        elif cycles_amount == SAFE_CYCLES:
            self.log(f"Getting average from last popularities")
            starting_popularity = thread_cycles.aggregate(total_sum=Sum('popularity')).get('total_sum')
            self.log(f"Got from aggregation {starting_popularity}")
            new_cycle_thread.popularity = starting_popularity / SAFE_CYCLES
            new_cycle_thread.save()
        else:
            last_id = max(c.id for c in CycleThread.objects.filter(thread=thread))

            self.log(f"Calculating from EMA from {last_id} cycle")
            previous_popularity = CycleThread.objects.get(id=last_id).popularity
            self.log(f"previous popularity {previous_popularity}")

            x = min(1.0, thread.all_files_size_mb / MAX_FILESIZE_PER_THREAD_MB)
            alpha_coefficent = MINIMUM_ALPHA_COEFFICENT + x * (MAXIMUM_ALPHA_COEFFICENT - MINIMUM_ALPHA_COEFFICENT)

            self.log(f"Alpha coefficent based on files {alpha_coefficent}")

            ema = self.calculate_ema(0.125, new_popularity, previous_popularity)
            if ema >= MINIMUM_POPULARITY:
                new_cycle_thread.popularity = ema
                self.log(f"Calculated from EMA {ema}")
                new_cycle_thread.save()
            else:
                pass
                self.delete_thread(thread)

    @staticmethod
    def previous_date():
        return timezone.now() - timedelta(minutes=SAFE_MINUTES)

    @staticmethod
    def delete_thread(thread: Thread):
        thread.delete()

    @staticmethod
    def calculate_ema(a_coefficent, new_popularity, previous_popularity):
        return a_coefficent * new_popularity + (1 - a_coefficent) * previous_popularity

    def calculate_popularity_from_new_entries(self, thread: Thread):
        entries = sorted(list(Entry.objects.filter(thread=thread)), key=lambda x: x.creation_date)
        return sum(
            self.get_entry_popularity(
                entry,
                [
                    entry
                    for entry in entries[:entries.index(entry)]
                    if entry.was_popularity_calculated
                ]
            )
            for entry in entries
            if not entry.was_popularity_calculated
        )

    def get_entry_popularity(self, entry: Entry, previous_entries: List[Entry]) -> float:
        entry.was_popularity_calculated = True
        entry.save()
        popularity = 0
        for calculator in ENTRY_POPULARITY_CALCULATORS:
            popularity = calculator(popularity, entry, previous_entries)

        self.log(f"Popularity from entry {entry}: {popularity}")
        return popularity
