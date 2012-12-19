#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imp
import importlib


class Module(object):

    @classmethod
    def load(cls, name):
        name, relative = name.split()
        try:
            module_path = importlib.import_module(name).__path__
        except AttributeError:
            return

        try:
            imp.find_module(relative, module_path)

        except ImportError:
            return

        return importlib.import_module(name)
