#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

os.environ["DJANGO_SETTINGS_MODULE"] = "shrine.settings"

from django.conf import settings

__all__ = ['settings']
