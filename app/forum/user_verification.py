import logging
import uuid
from dataclasses import dataclass
from typing import Optional

from django.contrib.auth.hashers import make_password, check_password

from Masquerade.settings import COOKIE_PASS, COOKIE_USER, COOKIE_LIFETIME
from forum.models import User


logger = logging.getLogger(__name__)


@dataclass
class Cookie:
    key: str
    value: str


@dataclass
class UserPassword:
    model: User
    password: str


def user_verification(func):
    def inner(*args, **kwargs):
        request = args[0].request
        if user := get_user(request):
            kwargs.update({"user": user})
        else:
            new_user = create_user()
            kwargs.update(
                {
                    "user": new_user.model,
                    "cookies_to_set": [
                        Cookie(COOKIE_USER, new_user.model.identifier),
                        Cookie(COOKIE_PASS, new_user.password),
                    ]
                }
            )
            logger.info(f"{new_user.model.identifier}: Created a new user")

        response = func(*args, **kwargs)

        for cookie in kwargs.get("cookies_to_set", []):
            response.set_cookie(cookie.key, cookie.value, COOKIE_LIFETIME)

        return response
    return inner


def get_user(request) -> Optional[User]:
    if COOKIE_USER in request.COOKIES and COOKIE_PASS in request.COOKIES:
        password = request.COOKIES[COOKIE_PASS]
        user_id = request.COOKIES[COOKIE_USER]
        logger.info(f"{user_id}: Verifying user")
        if user := verify_user(user_id, password):
            logger.info(f"{user}: User verified")
            return user
        logger.info(f"{user_id}: User verification failed")
    return None


def create_user() -> UserPassword:
    password = str(uuid.uuid4())
    new_user = User()
    hashed_password = make_password(
        password=password,
        salt=str(uuid.uuid4()),
        hasher="default",
    )
    new_user.password = hashed_password
    new_user.save()
    return UserPassword(model=new_user, password=password)


def verify_user(user_id: str, password: str) -> Optional[User]:
    try:
        user = User.objects.get(identifier=user_id)
        if check_password(password, user.password):
            return user
    except User.DoesNotExist:
        pass
    return None
