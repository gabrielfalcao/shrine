#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import envoy
import shutil
import optparse
from glob import glob
from os.path import dirname, join, abspath, realpath, basename, splitext
from shrine.loader import Module

from couleur import Shell

COMMANDS = []
SHRINE_FILE = lambda *path: abspath(join(dirname(realpath(__file__)), '..', *path))
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


class MetaCommand(type):
    def __init__(cls, name, bases, attrs):
        if name not in ('MetaCommand', 'Command'):
            shell = getattr(cls, 'shell', None)
            if not shell:
                raise SyntaxError('Commands have to define a "shell" attribute')

            COMMANDS.append((cls.shell, cls))

        return super(MetaCommand, cls).__init__(name, bases, attrs)


class Command(object):
    __metaclass__ = MetaCommand

    @classmethod
    def run_from_argv(cls, argv):
        for name in map(basename, glob(SHRINE_FILE('commands', '*.py'))):
            if name not in ('__init__.py', basename(__file__)):
                path = 'shrine.commands.{} *'.format(splitext(name)[0])
                Module.load(path)

        Command, args = cls.parse_argv(argv)
        return Command().run(args)

    @classmethod
    def parse_argv(cls, argv):
        parser = optparse.OptionParser(
            usage="%prog or type %prog -h (--help) for help",
            version='0.1.0')

        options, args = parser.parse_args(argv)

        if not args:
            raise SystemExit(1)

        command = args.pop(0)
        return cls.get_command(command, args), args

    @classmethod
    def get_command(cls, name, args):
        last_command = None
        menu = []
        for k, Command in COMMANDS:
            menu.append(k)
            if name == k:
                if last_command:
                    raise RuntimeError("Can't have two commands with the same `shell` declaration as name: {}.{} and {}.{}")

                last_command = Command

        if not last_command:
            raise RuntimeError("Could not find a command for `{}`.\nOptions include:\n{}".format(name, "\n".join(menu)))

        return last_command
