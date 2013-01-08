# -*- coding: utf-8 -*-

import dj_database_url
DEBUG = True
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


AUTHENTICATED_HOME = '/admin'

if PRODUCTION:
    EMAIL_BACKEND = 'shrine.mailgun.EmailBackend'
