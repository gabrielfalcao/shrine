#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

os.environ['SHRINE_SETTINGS_MODULE'] = 'settings'
from shrine.conf import settings

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

__all__ = ['settings']
