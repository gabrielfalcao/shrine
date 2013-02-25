#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from shrine.controllers import SessionRequestHandler
from shrine.routes import routes

self = sys.modules[__name__]


class Controller(SessionRequestHandler):
    def get(self, *args, **kw):
        return self.do_get(*args, **kw)

    def post(self, *args, **kw):
        return self.do_post(*args, **kw)

    def put(self, *args, **kw):
        return self.do_put(*args, **kw)

    def delete(self, *args, **kw):
        return self.do_delete(*args, **kw)

    def options(self, *args, **kw):
        return self.do_options(*args, **kw)

    def head(self, *args, **kw):
        return self.do_head(*args, **kw)

    def patch(self, *args, **kw):
        return self.do_patch(*args, **kw)


def make_controller(method, function, pattern, bases):
    # `r_` stands for "registered"
    BaseController = Controller
    pops = []
    for index, item in enumerate(routes):
        r_pattern, r_ctrl = item

        if r_pattern == pattern:
            BaseController = r_ctrl

            pops.append(item)

    map(routes.remove, pops)  # removing duplicate routes

    name = function.__name__.title() + method.title()
    parents = (BaseController, ) + tuple(bases)
    function_name = 'do_{}'.format(method.lower())
    return type(name, parents, {function_name: function})


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
