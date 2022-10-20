from .base import *
from ..env_utils import get_env

DEBUG = False
SECRET_KEY = get_env("DJANGO_SECRET_KEY")
STATIC_URL = get_env("DJANGO_STATIC_URL")
STATIC_ROOT = get_env("DJANGO_STATIC_ROOT")
ALLOWED_HOSTS = get_env("DJANGO_ALLOWED_HOSTS").split(",")

# https://docs.djangoproject.com/en/4.1/ref/databases/#mysql-notes
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "PORT": get_env("MYSQL_PORT"),
        "HOST": get_env("MYSQL_HOST"),
        "NAME": get_env("MYSQL_DB"),
        "USER": get_env("MYSQL_USER"),
        "PASSWORD": get_env("MYSQL_PASSWORD"),
    }
}
