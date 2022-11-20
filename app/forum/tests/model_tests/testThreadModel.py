from django.test import TestCase

from forum.models import Thread, Entry


class ThreadModelTests(TestCase):
    def setUp(self) -> None:
        self.thread1 = Thread.objects.create(title="Thread_1")
        self.thread2 = Thread.objects.create(title="Thread_2")
        Entry.objects.create(content="content", thread=self.thread1)
        self.date = Entry.objects.create(content="content", thread=self.thread1).creation_date

    def test_entries(self):
        self.assertEqual(self.thread1.entries_amount, 2)
        self.assertEqual(self.thread2.entries_amount, 0)

    def test_updated_date(self):
        self.assertEqual(self.thread1.update_date, self.date)
        self.assertEqual(self.thread2.update_date, self.thread2.created_date)

