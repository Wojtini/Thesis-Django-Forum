import re
import uuid
from typing import Optional, List

from django.db import models
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.utils.html import escape

from Masquerade.settings import DISPLAYABLE_IMAGES, DISPLAYABLE_VIDEOS


class User(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, null=False, primary_key=True, editable=False)
    display_name = models.CharField(null=True, default=None, editable=False, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    identicon = models.ImageField(null=False)

    @property
    def entries(self) -> QuerySet:
        return Entry.objects.filter(creator=self)

    @property
    def entries_amount(self) -> int:
        return len(self.entries)

    @property
    def threads(self) -> QuerySet:
        return Thread.objects.filter(creator=self)

    @property
    def threads_amount(self) -> int:
        return len(self.threads)

    @property
    def categories(self) -> QuerySet:
        return Category.objects.filter(creator=self)

    @property
    def categories_amount(self) -> int:
        return len(self.categories)

    def __str__(self) -> str:
        if self.display_name:
            return f"{self.display_name} : {self.identifier}"
        return f"{self.identifier}"


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=False, max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def is_empty(self) -> bool:
        return self.threads_amount == 0

    @property
    def threads_amount(self) -> int:
        return len(self.threads)

    @property
    def threads(self) -> QuerySet:
        return Thread.objects.filter(category=self)


class Thread(models.Model):
    title = models.CharField(max_length=64, unique=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title} by {str(self.creator)}"

    @property
    def entries_amount(self) -> int:
        return self.entries.count()

    @property
    def entries(self) -> Optional[QuerySet]:
        return Entry.objects.filter(thread=self).order_by("creation_date")

    @property
    def update_date(self):
        if self.entries:
            return self.entries.order_by("-creation_date")[0].creation_date
        return self.created_date

    @property
    def last_image(self) -> Optional["EntryFile"]:
        files_in_thread = EntryFile.objects.filter(entry__thread=self).order_by("entry__creation_date")
        images_in_thread = [
            file
            for file in files_in_thread
            if file.is_image
        ]
        if len(images_in_thread) > 0:
            return images_in_thread.pop()
        return None

    @property
    def get_link(self):
        return f"/thread/{self.title}"

    @property
    def all_files_size_b(self) -> int:
        files_in_thread = EntryFile.objects.filter(entry__thread=self)
        return sum(
            file.original_file.size + (file.compressed_file.size if file.compressed_file else 0)
            for file in files_in_thread
        )

    @property
    def all_files_size_kb(self) -> float:
        return self.all_files_size_b / 1024

    @property
    def all_files_size_mb(self) -> float:
        return round(self.all_files_size_kb / 1024, 2)


class EntryFile(models.Model):
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)
    original_file = models.FileField(null=True)
    compressed_file = models.FileField(null=True)

    def __str__(self):
        return f"{self.original_file.name}"

    @property
    def is_image(self):
        return any(
            str(self).endswith(extension)
            for extension in DISPLAYABLE_IMAGES
        )

    @property
    def is_video(self):
        return any(
            str(self).endswith(extension)
            for extension in DISPLAYABLE_VIDEOS
        )

    @property
    def thread_link(self):
        return self.entry.thread.get_link + f"#{self.entry.id}"


class Entry(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    was_popularity_calculated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.thread}: {self.content}"

    @property
    def attached_files(self):
        return EntryFile.objects.filter(entry=self).order_by("id")

    @property
    def with_links(self):
        regex = r"(#[0-9]+)"
        splitted = re.split(regex, self.content)
        result = [
            {
                "value": part if not re.search(regex, part) else f"<a href='{part}'>{part}</a>",
                "safe": re.search(regex, part),
            }
            for part in splitted
        ]
        return result

    @property
    def parsed(self):
        parts = self.with_links
        files: List[EntryFile] = list(self.attached_files)[::-1]
        s = [
            part.get("value") if part.get("safe") else escape(part.get("value"))
            for part in parts
        ]
        regex = r"(%)"
        splitted = re.split(regex, "".join(s))
        for index, part in enumerate(splitted):
            if re.search(regex, part):
                try:
                    splitted[index] = render_to_string(
                        "components/displayable_file.html",
                        context={"file": files.pop()},
                    )
                except IndexError:
                    break
        return "".join(splitted)

    @property
    def not_parsed_files(self):
        files: List[EntryFile] = list(self.attached_files)
        regex = r"(%)"
        amount_of_parsed_files = len(re.findall(regex, self.content))
        return files[amount_of_parsed_files:]


class Cycle(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} at {self.date}"


class CycleThread(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    popularity = models.FloatField()


all_models = [
    User, Entry, Thread, Category, EntryFile, Cycle, CycleThread
]
