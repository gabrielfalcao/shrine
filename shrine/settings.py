#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os import environ as ENV

from shrine.init import WORKING_DIR

PROJECT_PATH = lambda *path: os.path.join(WORKING_DIR, *path)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

PORT = int(ENV.get("PORT", 8000))
PRODUCTION = False

DATABASES = {
}

TIME_ZONE = "America/New_York"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


ROOT_URLCONF = "shrine.routes"

# Python dotted path to the WSGI application used by Django"s runserver.
WSGI_APPLICATION = "shrine.routes.wsgi"

TEMPLATE_PATH = PROJECT_PATH("templates")

INSTALLED_APPS = (
    "shrine.apps.core",
)
BROKER_BACKEND = "django"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },

    }
}

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
MAILGUN_ACCESS_KEY = "some-invalid-key"
MAILGUN_SERVER_NAME = "some-invalid-server-name"

EMAIL_FILE_PATH = PROJECT_PATH(".messages")
