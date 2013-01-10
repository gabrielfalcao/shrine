#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import importlib
import dj_database_url
from os import environ
database_url = dj_database_url


try:
    settings_module = environ['SHRINE_SETTINGS_MODULE']
except KeyError:
    raise RuntimeError('Shrine requires the environment variable SHRINE_SETTINGS_MODULE to be set to a module path')

user_settings = importlib.import_module(settings_module)
WORKING_DIR = os.path.abspath(os.path.dirname(user_settings.__file__))
LOCAL_FILE = lambda *path: os.path.join(WORKING_DIR, *path)
__alL__ = ['database_url', 'LOCAL_FILE', 'WORKING_DIR']
