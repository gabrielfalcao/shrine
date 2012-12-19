#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from shrine.loader import Module
from os.path import join, abspath, dirname

ws_settings_module = os.getenv('SHRIME_SETTINGS_MODULE')
if not ws_settings_module:
    raise ImportError(
        'Could not find the module {} inside {}'.format(
            ws_settings_module or 'SHRIME_SETTINGS_MODULE',
            os.getcwd()),
    )


from django.conf import settings

shrine_settings = Module.load(ws_settings_module)

for attr in dir(shrine_settings):
    setattr(settings, attr, getattr(shrine_settings, attr))


LOCAL_FILE = lambda *path: join(abspath(dirname(shrine_settings.__file__)), *path)

settings.LOCAL_FILE = LOCAL_FILE
sys.path.append(LOCAL_FILE('..'))
sys.path.append(LOCAL_FILE('apps'))
