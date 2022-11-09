from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Sum
from django.utils import timezone

from Masquerade.settings import SAFE_CYCLES, MINIMUM_POPULARITY
from forum.models import Thread, Entry, Cycle, CycleThread, User, Category


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Creating new cycle"))
        new_cycle = Cycle()
        new_cycle.save()
        threads = Thread.objects.filter(created_date__lte=self.previous_date())
        self.stdout.write(f"Got {len(threads)} thread(s)")
        for thread in threads:
            self.process_thread(new_cycle, thread)
        self.clear_empty_categories()
        self.clear_empty_users()

    def clear_empty_categories(self):
        categories_to_delete = [
            category
            for category in Category.objects.filter(created_date__lte=self.previous_date())
            if category.number_of_active_threads == 0
        ]
        for category in categories_to_delete:
            self.stdout.write(f"Deleting {category.name} empty category")
            # category.delete()

    def clear_empty_users(self):
        users_to_clear = [
            user
            for user in User.objects.filter(created_at__lte=self.previous_date())
            if user.threads_amount + user.categories_amount + user.entries_amount == 0
        ]
        for user in users_to_clear:
            self.stdout.write(f"Deleting {user} inactive user")
            # user.delete()

    def process_thread(self, cycle: Cycle, thread: Thread):
        self.stdout.write(f"Processing {thread}")
        new_popularity = self.calculate_popularity_from_new_entries(thread)
        if thread_cycles := CycleThread.objects.filter(thread=thread):
            cycles_amount = len(thread_cycles)
        else:
            cycles_amount = 0
        self.stdout.write(f"Thread in {cycles_amount} cycles")
        new_cycle_thread = CycleThread(cycle=cycle, thread=thread, popularity=0)
        if cycles_amount < SAFE_CYCLES:
            self.stdout.write(f"Setting new popularity for safe thread")
            new_cycle_thread.popularity = new_popularity
            new_cycle_thread.save()
        elif cycles_amount == SAFE_CYCLES:
            self.stdout.write(f"Getting average from last popularities")
            starting_popularity = thread_cycles.aggregate(total_sum=Sum('popularity')).get('total_sum')
            self.stdout.write(f"Got from aggregation {starting_popularity}")
            new_cycle_thread.popularity = starting_popularity / SAFE_CYCLES
            new_cycle_thread.save()
        else:
            last_id = max(c.id for c in CycleThread.objects.filter(thread=thread))

            self.stdout.write(f"Calculating from EMA from {last_id} cycle")
            previous_popularity = CycleThread.objects.get(id=last_id).popularity
            self.stdout.write(f"previous popularity {previous_popularity}")
            ema = self.calculate_ema(0.125, new_popularity, previous_popularity)
            if ema >= MINIMUM_POPULARITY:
                new_cycle_thread.popularity = ema
                self.stdout.write(f"Calculated from EMA {ema}")
                new_cycle_thread.save()
            else:
                pass
                # self.delete_thread(thread)

    @staticmethod
    def previous_date():
        return timezone.now() - timedelta(hours=1)

    @staticmethod
    def delete_thread(thread: Thread):
        thread.delete()

    @staticmethod
    def calculate_ema(a_coefficent, new_popularity, previous_popularity):
        return a_coefficent * new_popularity + (1 - a_coefficent) * previous_popularity

    def calculate_popularity_from_new_entries(self, thread: Thread):
        entries = Entry.objects.filter(thread=thread, calculated_popularity=False)
        return sum(
            self.get_entry_popularity(entry) for entry in entries
        )

    def get_entry_popularity(self, entry: Entry) -> float:
        amount_of_files = len(entry.attached_files)
        popularity = 2 + amount_of_files
        entry.calculated_popularity = True
        entry.save()
        self.stdout.write(f"Popularity from entry {entry}: {popularity}")
        return popularity
