import re
import uuid
from typing import Optional, List

from django.db import models
from django.db.models import QuerySet

from Masquerade.settings import DISPLAYABLE_IMAGES, DISPLAYABLE_VIDEOS


class User(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, null=False, primary_key=True, editable=False)
    display_name = models.CharField(null=True, default=None, editable=False, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    identicon = models.ImageField(null=False, editable=False)

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
    name = models.CharField(max_length=64, unique=True, editable=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    description = models.TextField(null=False, max_length=300, editable=False)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

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
    title = models.CharField(max_length=64, unique=True, editable=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    description = models.TextField(null=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, editable=False)
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
            file.size
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

    @property
    def size(self):
        try:
            return self.original_file.size
        except FileNotFoundError:
            return 0


class Entry(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    was_popularity_calculated = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"{self.thread}: {self.content}"

    @property
    def attached_files(self):
        return EntryFile.objects.filter(entry=self).order_by("id")

    @property
    def not_parsed_files(self):
        files: List[EntryFile] = list(self.attached_files)
        regex = r"<img"
        amount_of_parsed_files = len(re.findall(regex, self.content))//2
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
