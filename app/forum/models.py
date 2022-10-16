import uuid
from typing import Optional, Iterable

from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


class User(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, null=False, primary_key=True, editable=False)
    password = models.CharField(null=False, max_length=128)
    display_name = models.CharField(editable=False, max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

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
    def last_image(self) -> Optional["Image"]:
        entries_with_images = self.entries.exclude(attached_image__isnull=True)
        if last := entries_with_images.last():
            return last.attached_image
        return None


class Image(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    original_file = models.ImageField()
    thumbnail_file = models.ImageField(null=True)
    mini_file = models.ImageField(null=True)

    def __str__(self):
        return f"{self.original_file.name}"


class Entry(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    attached_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    replied_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.thread}: {self.content}"


all_models = [
    User, Entry, Thread, Category, Image
]
