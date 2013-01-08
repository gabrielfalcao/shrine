#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from shrine.controllers import SessionRequestHandler
from shrine.routes import routes

self = sys.modules[__name__]


class Controller(SessionRequestHandler):
    def get(self, *args, **kw):
        return self.do_get(self, *args, **kw)

    def post(self, *args, **kw):
        return self.do_post(self, *args, **kw)

    def put(self, *args, **kw):
        return self.do_put(self, *args, **kw)

    def delete(self, *args, **kw):
        return self.do_delete(self, *args, **kw)

    def options(self, *args, **kw):
        return self.do_options(self, *args, **kw)

    def head(self, *args, **kw):
        return self.do_head(self, *args, **kw)

    def patch(self, *args, **kw):
        return self.do_patch(self, *args, **kw)


def make_controller(method, function, pattern):
    name = function.__name__.title() + method.title()
    return type(name, (Controller,), {'do_{}'.format(method.lower()): function})


def make_responder(method):
    def responder(pattern):
        def dec(func):
            routes.append((pattern, make_controller(method, func, pattern)))

            return func
        return dec
    return responder

for method in 'get', 'post', 'put', 'delete', 'head', 'options', 'patch':
    setattr(self, method, make_responder(method))
