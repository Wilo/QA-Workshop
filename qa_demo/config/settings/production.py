from .base import *  # NoQA

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "NAME": "catalog",
        "ENGINE": "django.db.backends.postgresql",
        "USER": "catalog",
        "PASSWORD": "my_strong_and_secret_password",
        "HOST": "localhost",
        "PORT": 5432,
    }
}