# -*- coding: utf-8 -*-
import os
import dj_database_url

DEBUG = os.environ.get('PORT', None) is not None
TEMPLATE_DEBUG = DEBUG
PRODUCTION = not DEBUG

ADMINS = (
    (u'{username}', '{email}'),
)

MANAGERS = ADMINS
PRODUCT_NAME = '{shrine_name}'
APP_EMAIL_ADDRESS = 'emailer@{domain}'

DATABASES = {{
    'default': dj_database_url.config(
        default='sqlite://./{shrine_name}.sqlite')}}

TEMPLATE_PATH = './templates'
STATIC_PATH = './media'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
)
DOMAIN = '{domain}'

AUTHENTICATED_HOME = '/admin'
ENV_NAME = 'localhost'

if PRODUCTION:
    EMAIL_BACKEND = 'shrine.mailgun.EmailBackend'
    ENV_NAME = '{shrine_name}_production'

MAKE_FULL_URL = lambda x: 'http://{{0}}/{{1}}'.format(DOMAIN, x.lstrip('/'))
