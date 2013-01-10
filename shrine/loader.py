#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib


class Module(object):

    @classmethod
    def load(cls, name):
        return importlib.import_module(name)
