#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import logging
from glob import glob
from .registry import Command, join, basename, splitext

from tornado.ioloop import IOLoop
from tornado.web import Application
from shrine.loader import Module


class RunProject(Command):
    shell = 'run'

    def run(self, args):
        sys.path.insert(0, join(os.getcwdu(), '..'))
        os.environ['SHRINE_SETTINGS_MODULE'] = '{}.settings'.format(basename(os.getcwdu()))

        for name in map(basename, glob(join('controllers', '*.py'))):
            Module.load('{}.controllers.{} *'.format(basename(os.getcwdu()), splitext(name)[0]))

        from shrine.routes import routes

        from shrine import settings

        MESSAGE = "{} running at http://localhost:{}".format(
            settings.PRODUCT_NAME,
            settings.PORT,
        )

        application = Application(routes)

        application.listen(settings.PORT)
        print MESSAGE, routes
        from shrine.log import logger
        logger.setLevel(logging.WARNING)

        IOLoop.instance().start()
