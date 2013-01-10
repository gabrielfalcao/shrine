#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import envoy
import shutil
import hashlib
from functools import wraps
from glob import glob
from os.path import join, basename, exists
from shrine import version as shrine_version
from shrine.shell import sh, ballot, checkmark, arrow, SHRINE_FILE, logo

from .registry import Command


def abortable(func):
    @wraps(func)
    def wrapper(self, *args, **kw):
        try:
            return func(self, *args, **kw)
        except KeyboardInterrupt:
            return self.abort()
        except Exception as e:
            self.abort(failure=unicode(e))
            raise

    return wrapper


class CreateProject(Command):
    shell = 'create'

    # options
    should_create_git_repo = False
    should_create_heroku_app = False
    pwd = os.getcwdu()

    def ask_user_preferences(self):
        self.should_create_git_repo = self.ask_yn('Automatically create a git repository?', default='yes')
        self.should_create_heroku_app = self.ask_yn('Do you want heroku support ?', default='no')

    def ask_yn(self, question, default=''):
        default = default.lower()
        match = lambda r: r in ['y', 'n', 'yes', 'no']
        deftip = default.startswith('y') and '[Yn]' or '[yN]'

        ask = lambda: raw_input('\r\n{} {}'.format(question, deftip)).lower().strip()
        val = ''
        try:
            while not match(val):
                val = ask()
                if default and not match(val):
                    val = default
                    break

        except KeyboardInterrupt:
            print '\r'
            return self.abort()

        return val.startswith("y")

    def abort(self, failure=None):
        os.chdir(self.pwd)
        if not exists(self.project_name):
            return

        if failure:
            sh.bold_red_on_black("\r\nOOps, it broke :(\n\n{}\n".format(unicode(failure)))

        try:
            sh.bold_yellow_on_black("\r\nDo you want to remove the directory `{}` ?\n".format(self.project_name))
            if raw_input('(type "y" or "n"): ').lower().strip() == 'y':
                shutil.rmtree(self.project_name)

        except KeyboardInterrupt:
            sh.bold_red("Aborted without removing the directory `{}\n".format(self.project_name))

    @property
    def base_path(self):
        return join(os.getcwdu(), self.project_name)

    def project_file(self, *path):
        return join(self.base_path, *path)

    @abortable
    def new_file(self, name):
        return open(self.project_file(name), 'w')

    @abortable
    def skel_file(self, name):
        return open(SHRINE_FILE('skel', name), 'r')

    def get_context(self):
        username = os.environ.get('USER', 'user')
        domain = '{}.io'.format(self.project_name)

        fallback_email = '{username}@{domain}'.format(**locals())
        email = os.environ.get('EMAIL', fallback_email)
        sha512 = hashlib.sha512()
        sha512.update(self.project_name)
        sha512.update(username)
        sha512.update(domain)

        context = {
            'shrine_name': self.project_name,
            'username': username,
            'email': email,
            'domain': domain,
            'salt': sha512.hexdigest(),
            'shrine_tmp_dir': self.shrine_tmp_dir,
            'shrine_version': shrine_version,
        }

        return context

    @abortable
    def create_file(self, name):
        context = self.get_context()

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

    @abortable
    def clone_dir(self, name):
        sh.bold_white_on_black(u'Creating ')
        sh.bold_cyan_on_black(self.project_file(name))
        context = self.get_context()

        try:
            shutil.copytree(SHRINE_FILE('skel', name), self.project_file(name))

            for filename in glob(self.project_file(name, '*.html')):
                contents = open(filename).read()
                for name in context:
                    variable = '@{}@'.format(name)
                    contents = contents.replace(variable, context[name])

                open(filename, 'w').write(contents)
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
        sh.dedent()

    def run(self, args):
        if not args:
            sh.bold_white_on_black("USAGE: ")
            sh.bold_green_on_black("shrine create name_of_the_project\n")
            raise SystemExit(1)

        self.project_name = unicode(args.pop(0)).strip()
        self.project_path = join(self.pwd, self.project_name)
        self.shrine_tmp_dir = '{}_temp'.format(self.project_name)

        if os.path.exists(self.project_name):
            sh.bold_red_on_black("{} already exists\n".format(self.project_name))
            print
            raise SystemExit(1)

        if not re.search(r'^[a-zA-Z][\w_]+$', self.project_name):
            example = re.sub(r'^[\W0-9]+', '', self.project_name)
            example = ''.join(re.findall(r'^[a-zA-Z]\w+', example)) or 'project_name'

            sh.bold_red_on_black("Invalid shrine name: {}\n".format(self.project_name))
            sh.bold_white_on_black("Please use a valid python package name\n")
            sh.bold_white_on_black("Example: ")
            sh.bold_green_on_black(example)
            print
            raise SystemExit(1)

        self.ask_user_preferences()
        sh.bold_yellow_on_black("Creating `{}`...".format(self.project_name))

        templates = [
            SHRINE_FILE('skel/README.md'),
            SHRINE_FILE('skel/Procfile'),
            SHRINE_FILE('skel/requirements.txt'),
            SHRINE_FILE('skel/.gitignore'),
        ]
        templates.extend(glob(SHRINE_FILE('skel/*.py')))

        os.makedirs(self.project_name)

        tmp_dir_path = join(self.project_name, self.shrine_tmp_dir)
        os.makedirs(tmp_dir_path)

        for template in templates:
            name = basename(template)
            self.create_file(name)

        static_dirs = [
            SHRINE_FILE('skel/media'),
            SHRINE_FILE('skel/templates'),
            SHRINE_FILE('skel/controllers'),
        ]

        for path in static_dirs:
            self.clone_dir(basename(path))

        sh.bold_yellow_on_black(logo)
        print

        self.create_git_repository()
        self.prepare_for_heroku()
        sh.bold_green_on_black('now execute:\n\n')
        sh.bold_white_on_black('  cd {}\n'.format(self.project_name))
        sh.bold_white_on_black('  shrine run\n')

    def create_git_repository(self):
        if not self.should_create_git_repo:
            return

        os.chdir(self.project_path)
        if envoy.run('which git').status_code is 0:
            sh.bold_red_on_black('Attempting to create git repository...')
            os.system('git init')
            os.system('git add .')
            sh.bold_green(checkmark)
        else:
            sh.bold_red_on_black('Git is not installed, ignoring initialization of repository\n')

    def prepare_for_heroku(self):
        if not self.should_create_heroku_app:
            return

        os.chdir(self.project_path)
        response = envoy.run('heroku version')
        if response and 'toolbelt' in response.std_out:
            sh.bold_red_on_black('Creating heroku app...\n')
            r = envoy.run("heroku create")

            if r.status_code is 0:
                sh.bold_green('\n{}\n'.format(r.std_out))
            else:
                sh.bold_red('\n{}\n{}'.format(r.std_out, r.std_err))

        else:
            sh.bold_red_on_black('Heroku toolbelt is not installed.\n')
            sh.bold_white_on_black('More info: http://toolbelt.heroku.com')
