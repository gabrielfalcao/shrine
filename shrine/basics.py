#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tempfile
import subprocess


DEPENDENCIES = {
    'couleur': None,
    'envoy': None,
    'Django': '1.5',
    'tornado': '2.4.1',
    'psycopg2': None,
    'south': '0.7.6',
    'requests': '1.1.0',
}


class DependencyResolver(object):
    output = tempfile.NamedTemporaryFile()

    @classmethod
    def shell(self, command):
        return subprocess.Popen(command, shell=True)

    @classmethod
    def get_dependencies(self, error):
        return [(d, DEPENDENCIES[d]) for d in sorted(DEPENDENCIES) if d.lower() in unicode(error).lower()]

    @classmethod
    def check(self, error):
        dependencies = self.get_dependencies(error)

        for dependency, v in dependencies:
            version = v and '=={0}'.format(v) or ''

            command = 'pip install {0}{1}'.format(dependency, version)
            print 'shrine needs', dependency, "which is missing"
            print 'installing', v or ''
            print command
            print "." * len(command)
            self.shell(command).communicate(sys.stdin)
            print "." * len(command)

        if len(dependencies) is 0:
            raise error
        else:
            print "=" * 10
            print "Shrine finished installing its dependencies, please run the command below again:"
            print " ".join(sys.argv)
            return True
