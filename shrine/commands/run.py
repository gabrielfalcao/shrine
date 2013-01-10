#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from glob import glob
from os.path import join, basename, splitext
from couleur import Shell
from .registry import Command

from tornado.ioloop import IOLoop
from shrine.loader import Module
from tornado import autoreload

sh = Shell()


class RunProject(Command):
    shell = 'run'

    current_dir_name = basename(os.getcwdu())

    def get_settings(self):
        os.environ['SHRINE_SETTINGS_MODULE'] = '{}.settings'.format(basename(os.getcwdu()))
        from shrine.conf import settings
        return settings

    def run(self, args):
        settings = self.get_settings()

        for name in map(basename, glob(join('controllers', '*.py'))):
            autoreload.watch(name)
            Module.load(self.get_controller_import_path(name))

        from shrine.routes import make_application

        MESSAGE = "{} running at http://localhost:{}".format(
            settings.PRODUCT_NAME,
            settings.PORT,
        )

        application = make_application()
        application.listen(settings.PORT)
        print MESSAGE

        from shrine.log import logger
        logger.setLevel(logging.WARNING)

        try:
            IOLoop.instance().start()
        except KeyboardInterrupt:
            sh.bold_red_on_black("\rInterrupted by the User (Control-C)\n")

    def get_controller_import_path(self, name):
        return '{}.controllers.{}'.format(self.current_dir_name,
                                          self.remove_extension(name))

    def remove_extension(self, name):
        return splitext(name)[0]


class RunInProduction(RunProject):
    shell = 'run:production'

    def run(self, args):
        settings = self.get_settings()
        if not settings.DEBUG:
            return super(RunInProduction, self).run(args)

        print "Cannot run in production because settings.DEBUG is True"
        raise SystemExit(1)
