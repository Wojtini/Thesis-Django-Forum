import uuid

from django.db import models
from django.db.models import QuerySet, Sum
from django.utils import timezone


class User(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, null=False, primary_key=True, editable=False)
    password = models.CharField(null=False, max_length=128)
    display_name = models.CharField(editable=False, max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def entries(self) -> QuerySet:
        return Entry.objects.filter(creator=self)

    @property
    def points(self) -> int:
        return sum(item.points for item in self.entries)

    def __str__(self) -> str:
        return f"{name if (name := self.display_name) else 'NO_NAME'}: {self.identifier}"


class Category(models.Model):
    name = models.CharField(max_length=64)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

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


class Thread(models.Model):
    title = models.CharField(max_length=64)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title} by {str(self.creator)}"

    @property
    def points(self) -> int:
        return sum(abs(entry) for entry in Entry.objects.filter(thread=self))

    @property
    def total_number_of_entries(self) -> int:
        return self.entries.count()

    @property
    def entries(self):
        return Entry.objects.filter(thread=self)

    @property
    def update_date(self):
        return self.entries.order_by("-update_date")[0].update_date


class Image(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    original_file = models.ImageField()
    compressed_file = models.ImageField(null=True)

    def __str__(self):
        return f"{self.original_file.name}"


class Entry(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    attached_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    replied_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.thread}: {self.content}"

    @property
    def reviews(self) -> QuerySet:
        return Review.objects.filter(entry=self)

    @property
    def points(self) -> int:
        return self.reviews.aggregate(Sum("points"))['points__sum']


class Review(models.Model):
    points = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "entry")

    def __str__(self):
        return f"{self.id}"


all_models = [
    User, Entry, Review, Thread, Category, Image
]
