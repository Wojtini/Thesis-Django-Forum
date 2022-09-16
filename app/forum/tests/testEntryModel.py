from django.test import TestCase

from forum.models import Category, Thread, Entry, Review
from forum.user_verification import create_user


class EntryModelTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user().model
        self.thread = Thread()
        self.thread.save()
        self.entry = Entry(thread=self.thread)
        self.entry.save()
        self.review = Review(entry=self.entry, points=222, user=self.user)
        self.review.save()

    def test_get_entries(self):
        self.assertEqual(self.entry.points, 222)
