#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
os.environ['SHRINE_SETTINGS_MODULE'] = '{shrine_name}.settings'
from shrine.conf import settings

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

__all__ = ['settings']
