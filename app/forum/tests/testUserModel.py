from django.test import TestCase

from forum.user_verification import create_user, verify_user


class UserModelTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user()

    def test_user_verification(self):
        user_id = self.user.model.identifier
        password = self.user.password
        self.assertTrue(verify_user(user_id=user_id, password=password))
