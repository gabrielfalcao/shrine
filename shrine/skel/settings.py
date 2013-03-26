# -*- coding: utf-8 -*-
import os
from shrine.init import dj_database_url

DEBUG = not os.getenv("PORT")
TEMPLATE_DEBUG = DEBUG
PRODUCTION = not DEBUG

ADMINS = (
    (u"{username}", "{email}"),
)

MANAGERS = ADMINS
PRODUCT_NAME = "{shrine_name}"
APP_EMAIL_ADDRESS = "emailer@{domain}"

DATABASES = {{
    "default": dj_database_url.config(
        default="sqlite://./{shrine_name}.sqlite")}}

if PRODUCTION:
    DATABASES['default']['OPTIONS'] = {{
        'autocommit': True,
    }}

TEMPLATE_PATH = "./templates"
STATIC_PATH = "./media"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
)
DOMAIN = "{domain}"

AUTHENTICATED_HOME = "/"
ANONYMOUS_HOME = "/"

ENV_NAME = "localhost"

TORNADO_CONFIG = {{
    'login_url': '/login',
    'cookie_secret': "{salt}",
}}


if PRODUCTION:
    EMAIL_BACKEND = "shrine.mailgun.EmailBackend"
    ENV_NAME = "{shrine_name}_production"

MAKE_FULL_URL = lambda x: "http://{{0}}/{{1}}".format(DOMAIN, x.lstrip("/"))
