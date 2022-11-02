import logging
import os
import uuid
from dataclasses import dataclass
from typing import Optional
import jwt
import pydenticon
from django.core.exceptions import ObjectDoesNotExist
from jwt import InvalidSignatureError

from Masquerade.settings import COOKIE_NAME_JWT, COOKIE_LIFETIME, MEDIA_ROOT, IDENTICON_SIZE, \
    IDENTICON_PADDING, IDENTICON_BACKGROUND, IDENTICON_FOREGROUNDS, SECRET_KEY
from forum.models import User


logger = logging.getLogger(__name__)


@dataclass
class Cookie:
    key: str
    value: str


@dataclass
class UserJWT:
    model: User
    encoded_jwt: str


def user_verification(user_needed):
    def outer(func):
        def inner(*args, **kwargs):
            request = args[0].request
            if user := get_user(request):
                kwargs.update({"user": user})
            elif user_needed:
                new_user = create_user()
                kwargs.update(
                    {
                        "user": new_user.model,
                        "cookies_to_set": [
                            Cookie(COOKIE_NAME_JWT, new_user.encoded_jwt),
                        ]
                    }
                )
                logger.info(f"{new_user.model.identifier}: Created a new user")

            response = func(*args, **kwargs)

            for cookie in kwargs.get("cookies_to_set", []):
                response.set_cookie(cookie.key, cookie.value, COOKIE_LIFETIME)

            return response
        return inner
    return outer


def get_user(request) -> Optional[User]:
    if COOKIE_NAME_JWT in request.COOKIES:
        user_jwt = request.COOKIES[COOKIE_NAME_JWT]
        try:
            return verify_user(user_jwt)
        except ObjectDoesNotExist:
            pass
    return None


def verify_user(user_jwt) -> Optional[User]:
    try:
        decoded = jwt.decode(user_jwt, SECRET_KEY, algorithms=["HS256"])
        logger.info(f"User verified")
        return User.objects.get(identifier=decoded.get("identifier"))
    except InvalidSignatureError:
        logger.info(f"User verification failed")
        return None


def create_user() -> UserJWT:
    new_user = User()
    new_user.identicon = create_identicon(new_user.identifier)
    new_user.save()
    payload = {
        "identifier": str(new_user.identifier)
    }
    encoded = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return UserJWT(model=new_user, encoded_jwt=encoded)


def create_identicon(username: uuid.UUID) -> str:
    username = str(username)
    username = "".join(username.split("-"))
    logger.info(f"Creating new identicon for {username}")
    size_x, size_y = IDENTICON_SIZE
    generator = pydenticon.Generator(
        size_x,
        size_y,
        foreground=IDENTICON_FOREGROUNDS,
        background=IDENTICON_BACKGROUND,
    )
    identicon = generator.generate(username, 200, 200, output_format="png", padding=IDENTICON_PADDING)
    filepath = os.path.join(MEDIA_ROOT, f"{username}.png")
    with open(filepath, "wb") as file:
        file.write(identicon)
    logger.info(f"Created new identicon at {filepath}")
    return f"{username}.png"
