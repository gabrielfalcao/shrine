#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
os.environ['SHRIME_SETTINGS_MODULE'] = 'settings'
from shrine import settings

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

__all__ = ['settings']
