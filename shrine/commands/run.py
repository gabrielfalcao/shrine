#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from glob import glob
from os.path import join, basename, splitext
from .registry import Command

from tornado.ioloop import IOLoop
from shrine.loader import Module
from tornado import autoreload


class RunProject(Command):
    shell = 'run'

    current_dir_name = basename(os.getcwdu())

    def run(self, args):

        os.environ['SHRINE_SETTINGS_MODULE'] = '{}.settings'.format(basename(os.getcwdu()))
        from shrine.conf import settings

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

        IOLoop.instance().start()

    def get_controller_import_path(self, name):
        return '{}.controllers.{}'.format(self.current_dir_name,
                                          self.remove_extension(name))

    def remove_extension(self, name):
        return splitext(name)[0]