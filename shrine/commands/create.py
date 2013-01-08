#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .registry import *



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

        if envoy.run('which git').status_code is 0:
            sh.bold_red_on_black('Attempting to create git repository...')
            r = envoy.run("cd {} && git init && git add .".format(self.project_name))
            if r.status_code is 0:
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
