#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .registry import ShellCommand


class Syncdb(ShellCommand):
    shell = 'syncdb'
