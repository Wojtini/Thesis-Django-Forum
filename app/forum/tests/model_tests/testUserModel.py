from django.test import TestCase

from forum.decorators.user_verification import create_user, verify_user, UserJWT


class UserModelTests(TestCase):
    def setUp(self) -> None:
        self.user: UserJWT = create_user()

    def test_user_verification(self):
        user_id = self.user.model.identifier
        verified_user = verify_user(self.user.encoded_jwt)
        self.assertTrue(verified_user.identifier == user_id)
