import os

import dj_database_url

from .base import *

DEBUG = False

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL", False), conn_max_age=600
    )
}

MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware"] + MIDDLEWARE
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MAX_AGE = 604800 * 2  # 2 weeks

SECRET_KEY = os.environ.get("SECRET_KEY", None)

ALLOWED_HOSTS = [
    "*",
]  # * to test on DO

# force https on heroku
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        }
    },
}


# BASE_DIR = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_URL = '/static/'
