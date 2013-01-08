#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import optparse
import commands
from glob import glob
from os.path import dirname, join, abspath, basename, realpath
from couleur import Shell

COMMANDS = []
SHRINE_FILE = lambda *path: abspath(join(dirname(realpath(__file__)), *path))
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


class CreateProject(Command):
    shell = 'create'

    @property
    def base_path(self):
        return os.path.join(os.getcwdu(), self.project_name)

    def project_file(self, name):
        return join(self.base_path, name)

    def new_file(self, name):
        return open(self.project_file(name), 'w')

    def skel_file(self, name):
        return open(SHRINE_FILE('skel', name), 'r')

    def create_file(self, name):
        sh = Shell(indent=2)
        username = os.environ.get('USER', 'user')
        domain = '{}.io'.format(self.project_name)

        fallback_email = '{username}@{domain}.io'.format(**locals())
        email = os.environ.get('EMAIL', fallback_email)

        context = {
            'shrine_name': self.project_name,
            'username': username,
            'email': email,
            'domain': domain,
        }

        with self.new_file(name) as destination:
            with self.skel_file(name) as view:
                sh.bold_white_on_black(u'Creating ')
                sh.bold_green_on_black(self.project_file(name))

                try:
                    body = view.read()
                    inside = body.format(**context)
                    destination.write(inside)
                except:
                    sh.bold_red(ballot)
                    raise
                else:
                    sh.bold_green(checkmark)

    def clone_dir(self, name):
        sh = Shell(indent=2)
        sh.bold_white_on_black(u'Creating ')
        sh.bold_cyan_on_black(self.project_file(name))

        try:
            shutil.copytree(SHRINE_FILE('skel', name), self.project_file(name))
        except:
            sh.bold_red_on_black(ballot)
            raise
        else:
            sh.bold_green_on_black(checkmark)

        sh.indent()
        for path in glob(self.project_file(join(name, '*'))):
            sh.bold_white(arrow)
            sh.bold_green_on_black(path)
            print

    def run(self, args):
        sh = Shell(indent=0)

        self.project_name = args.pop(0)
        print sh.bold_yellow_on_black("Creating `{}`...".format(self.project_name))

        templates = [
            SHRINE_FILE('skel/README.md'),
            SHRINE_FILE('skel/Procfile'),
            SHRINE_FILE('skel/requirements.pip'),
        ]
        templates.extend(glob(SHRINE_FILE('skel/*.py')))

        os.makedirs(self.project_name)
        for template in templates:
            name = basename(template)
            self.create_file(name)

        static_dirs = [
            SHRINE_FILE('skel/media'),
            SHRINE_FILE('skel/templates'),
        ]

        for path in static_dirs:
            self.clone_dir(basename(path))

        sh.bold_yellow_on_black(logo)
        print

        if commands.getstatusoutput('which git')[0] is 0:
            sh.bold_red_on_black('Attempting to create git repository')
            code, out = commands.getstatusoutput("cd {} && git init && git add .".format(self.project_name))
            if code is 0:
                sh.bold_green(checkmark)
            else:
                sh.bold_red(ballot)

        sh.bold_green_on_black('now execute:\n\n')
        sh.bold_white_on_black('cd {} && shrine run\n'.format(self.project_name))


def main():
    exit_code = Command.run_from_argv(sys.argv[1:])
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
