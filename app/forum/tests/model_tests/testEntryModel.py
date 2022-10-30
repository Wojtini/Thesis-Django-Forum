from django.test import TestCase

from forum.models import Thread, Entry
from forum.user_verification import create_user


class EntryModelTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user().model
        self.thread = Thread()
        self.thread.save()
        self.entry = Entry(thread=self.thread)
        self.entry.save()

    def test_get_entries(self):
        self.assertEqual(self.thread.total_number_of_entries, 1)
