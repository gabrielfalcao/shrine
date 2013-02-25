#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import autoreload

from glob import glob
from os.path import join, basename, splitext

from shrine.loader import Module

module_cache = []


class ControllerLoader(object):
    def __init__(self, working_dir):
        self.package = basename(working_dir)

    def get_controller_import_path(self, name):
        return '{}.controllers.{}'.format(self.package,
                                          self.remove_extension(name))

    def seek_and_destroy(self):
        for name in map(basename, glob(join('controllers', '*.py'))):
            module_cache.append(
                Module.load(self.get_controller_import_path(name)))
            autoreload.watch(name)

    def remove_extension(self, name):
        return splitext(name)[0]
