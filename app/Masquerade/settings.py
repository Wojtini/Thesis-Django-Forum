from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG_MODE") == "True"

ALLOWED_HOSTS = ["milepogawedki.xyz", "www.milepogawedki.xyz", "localhost", "192.168.1.2"]
CSRF_TRUSTED_ORIGINS = ["https://milepogawedki.xyz"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "forum.apps.ForumConfig",
    "django_crontab",
    "channels",
    "captcha",
    "compressor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "Masquerade.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Masquerade.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_NAME"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

COMPRESS_PRECOMPILERS = (
    ("text/x-scss", "django_libsass.SassCompiler"),
)

COMPRESS_OFFLINE = not DEBUG
LIBSASS_OUTPUT_STYLE = "compressed"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "../staticfiles")

MEDIA_ROOT = os.path.join(BASE_DIR, "../media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CHANNELS

ASGI_APPLICATION = "Masquerade.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

# CACHES

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
    }
}
DISABLE_CACHE = DEBUG
GALLERY_CACHE = "gallery_cache"
FILE_LIST_CACHE = "file_list_cache"
USER_LIST_CACHE = "user_list_cache"
INDEX_CACHE = "index_cache"
THREAD_CACHE = "thread_cache"

# COOKIES NAMES

COOKIE_NAME_JWT = "identificator"
COOKIE_LIFETIME = 365*24*60*60

# CRONJOBS

CRONJOBS = [
    ('*/1 * * * *', 'forum.cron.my_scheduled_job', '>> /app/app/scheduled_job.log')
]


# IDENTICON

IDENTICON_FOREGROUNDS = [
    "rgb(45,79,255)",
    "rgb(254,180,44)",
    "rgb(226,121,234)",
    "rgb(30,179,253)",
    "rgb(232,77,65)",
    "rgb(49,203,115)",
    "rgb(141,69,170)",
]
IDENTICON_BACKGROUND = "rgb(224,224,224)"
IDENTICON_PADDING = (10, 10, 10, 10)
IDENTICON_SIZE = (10, 10)

# DISPLAYABLE MEDIA
DISPLAYABLE_IMAGES = [".png", ".jpg", ".gif", ".webp"]
DISPLAYABLE_VIDEOS = [".mp4"]
