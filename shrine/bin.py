#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from shrine.commands.registry import Command


def main():
    exit_code = Command.run_from_argv(sys.argv[1:])
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
