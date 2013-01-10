#!/usr/bin/env python
# -*- coding: utf-8 -*-
import envoy
import shutil
from couleur import Shell
from os.path import dirname, abspath, join, realpath

ballot = ' \xe2\x9c\x98\n'
checkmark = ' \xe2\x9c\x94\n'
arrow = ' \xe2\x9e\x99'


logo = """
         dP                oo
         88
.d8888b. 88d888b. 88d888b. dP 88d888b. .d8888b.
Y8ooooo. 88'  `88 88'  `88 88 88'  `88 88ooood8
      88 88    88 88       88 88    88 88.  ...
`88888P' dP    dP dP       dP dP    dP `88888P'
"""


sh = Shell(indent=2)
SHRINE_FILE = lambda *path: abspath(join(dirname(realpath(__file__)), *path))

__all__ = ['sh', 'logo', 'arrow', 'checkmark', 'ballot', 'shutil', 'envoy', 'SHRINE_FILE']
