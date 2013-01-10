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


def make_controller(method, function, pattern, bases):
    name = function.__name__.title() + method.title()
    parents = (Controller, ) + tuple(bases)
    name = 'do_{}'.format(method.lower())
    return type(name, parents, {name: function})


def make_responder(method, bases1=()):
    def responder(pattern, bases2=()):
        def dec(func):
            bases = tuple(bases1) + tuple(bases2)
            ctrl = make_controller(method, func, pattern, bases)
            routes.append((pattern, ctrl))

            return func
        return dec
    return responder


def mount_responder_factory(obj, bases=()):
    for method in 'get', 'post', 'put', 'delete', 'head', 'options', 'patch':
        setattr(obj, method, make_responder(method, bases))

    return obj

mount_responder_factory(self)
