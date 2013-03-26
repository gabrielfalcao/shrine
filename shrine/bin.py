#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from shrine.basics import DependencyResolver

try:
    from shrine.cmds.registry import Command
    check = True
except ImportError as e:
    DependencyResolver.check(e)
    check = False


def execute():
    has_dependencies = True
    while has_dependencies:
        try:
            exit_code = Command.run_from_argv(sys.argv[1:])
            has_dependencies = False
        except ImportError as e:
            has_dependencies = DependencyResolver.check(e)

    sys.exit(exit_code)

if __name__ == '__main__':
    check and execute()
