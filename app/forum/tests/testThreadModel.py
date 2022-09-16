import pytz
from django.test import TestCase

from forum.models import Thread, Entry
from datetime import datetime


class ThreadModelTests(TestCase):
    def setUp(self) -> None:
        thread = Thread.objects.create(title="Thread_1")
        self.time1 = datetime(2012, 12, 25, 0, 0, 0, 0, tzinfo=pytz.UTC)
        self.time2 = datetime(2000, 12, 25, 0, 0, 0, 0, tzinfo=pytz.UTC)
        Entry.objects.create(content="content", thread=thread, update_date=self.time1)
        Entry.objects.create(content="content", thread=thread, update_date=self.time2)

    def test_last_update_date(self):
        thread = Thread.objects.get(title="Thread_1")
        result = thread.update_date.date() - self.time1.date()
        self.assertEqual(result.total_seconds(), 0)
