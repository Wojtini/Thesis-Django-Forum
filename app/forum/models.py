import os
import re
import uuid
from typing import Optional, Iterable

from django.db import models
from django.db.models import QuerySet

from Masquerade.settings import DISPLAYABLE_IMAGES, DISPLAYABLE_VIDEOS


class User(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, null=False, primary_key=True, editable=False)
    password = models.CharField(null=False, max_length=128)
    display_name = models.CharField(editable=False, max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    identicon = models.ImageField(null=False)

    @property
    def entries(self) -> QuerySet:
        return Entry.objects.filter(creator=self)

    def __str__(self) -> str:
        return f"{name if (name := self.display_name) else 'NO_NAME'}: {self.identifier}"


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=False, max_length=300)

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def is_empty(self) -> bool:
        return self.number_of_active_threads == 0

    @property
    def number_of_active_threads(self) -> int:
        return len(self.threads)

    @property
    def threads(self) -> QuerySet:
        return Thread.objects.filter(category=self)

    @staticmethod
    def all_non_empty() -> Iterable['Category']:
        return Category.objects.all()


class Thread(models.Model):
    title = models.CharField(max_length=64, unique=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    indexed = models.BooleanField(verbose_name="Is indexed")

    def __str__(self) -> str:
        return f"{self.title} by {str(self.creator)}"

    @property
    def total_number_of_entries(self) -> int:
        return self.entries.count()

    @property
    def entries(self) -> Optional[QuerySet]:
        return Entry.objects.filter(thread=self)

    @property
    def update_date(self):
        if self.entries:
            return self.entries.order_by("-creation_date")[0].creation_date
        return self.created_date

    @property
    def last_image(self) -> Optional["EntryFile"]:
        files_in_thread = EntryFile.objects.filter(entry__thread=self)
        images_in_thread = [
            file
            for file in files_in_thread
            if file.is_image
        ]
        if len(images_in_thread) > 0 and (last := images_in_thread.pop()):
            return last
        return None


class EntryFile(models.Model):
    original_file = models.FileField(null=True)
    compressed_file = models.FileField(null=True)

    def __str__(self):
        return self.original_file.name

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


class Entry(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    attached_files = models.ManyToManyField(EntryFile)
    replied_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.thread}: {self.content}"

    @property
    def with_links(self):
        result = self.content
        splitted = re.findall(r"#[0-9]+", self.content)
        for link in splitted:
            result = result.replace(link, f"<a href='#{link[1:]}'>{link}</a>")
        return result


all_models = [
    User, Entry, Thread, Category, EntryFile
]
