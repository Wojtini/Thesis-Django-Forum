from django.test import TestCase

from forum.models import Thread, Entry, Review
from forum.user_verification import create_user, verify_user


class UserModelTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.user_2 = create_user()
        self.thread = Thread(title="Test", creator=self.user.model)
        self.thread.save()

        self.entries = [
            [20, 40, 10, 100]
        ]
        for entry in self.entries:
            for review_points in entry:
                entry = Entry(thread=self.thread, creator=self.user.model)
                entry.save()
                Review(entry=entry, points=review_points, user=self.user_2.model).save()

    def test_user_creation(self):
        user_id = self.user.model.identifier
        password = self.user.password
        self.assertTrue(verify_user(user_id=user_id, password=password))

    def test_user_points_aggregator(self):
        self.assertEqual(
            self.user.model.points,
            sum(element for tab in self.entries for element in tab)
        )
