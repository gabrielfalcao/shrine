#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from shrine.loader import Module
from os.path import join, abspath, dirname


os.environ['DJANGO_SETTINGS_MODULE'] = 'shrine.settings'
ws_settings_module = os.getenv('SHRINE_SETTINGS_MODULE')
if not ws_settings_module:
    raise ImportError(
        'Could not find the module {} inside {}'.format(
            ws_settings_module or 'SHRINE_SETTINGS_MODULE',
            os.getcwd()),
    )


from django.conf import settings as django_settings

SUBDIR = join(os.getcwdu(), '..')
sys.path.insert(0, SUBDIR)
shrine_settings = Module.load(ws_settings_module)
sys.path.remove(SUBDIR)

for settings_key in dir(shrine_settings):

    if settings_key.startswith('__'):
        continue
    settings_value = getattr(shrine_settings, settings_key)
    if settings_key == 'DATABASES':
        django_settings.DATABASES.update(settings_value)

    elif settings_key in ('INSTALLED_APPS',):
        django_settings.INSTALLED_APPS = tuple(set(django_settings.INSTALLED_APPS + settings_value))

    elif settings_key in ('TEMPLATE_PATH', 'STATIC_PATH',):
        setattr(django_settings, settings_key, django_settings.PROJECT_PATH(settings_value))

    else:
        setattr(django_settings, settings_key, settings_value)

LOCAL_FILE = lambda *path: join(abspath(dirname(shrine_settings.__file__)), *path)
django_settings.LOCAL_FILE = LOCAL_FILE
sys.path.append(LOCAL_FILE('..'))
