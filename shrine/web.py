#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from shrine.controllers import SessionRequestHandler
from shrine.routes import routes

from shrine.conf import settings
self = sys.modules[__name__]

HTTP_METHODS = ['get', 'post', 'put', 'delete', 'head', 'options', 'patch']


class Controller(SessionRequestHandler):
    def perform(self, method, args, kwargs):
        if self.requires_authentication and not self.user:
            if self.request.path != settings.ANONYMOUS_HOME:
                return self.redirect(settings.ANONYMOUS_HOME)
            else:
                return self.finish('You should not be here')

        responder = getattr(self, 'do_{0}'.format(method))
        return responder(*args, **kwargs)

    def get(self, *args, **kw):
        return self.perform('get', args, kw)

    def post(self, *args, **kw):
        return self.perform('post', args, kw)

    def put(self, *args, **kw):
        return self.perform('put', args, kw)

    def delete(self, *args, **kw):
        return self.perform('delete', args, kw)

    def options(self, *args, **kw):
        return self.perform('options', args, kw)

    def head(self, *args, **kw):
        return self.perform('head', args, kw)

    def patch(self, *args, **kw):
        return self.perform('patch', args, kw)


def make_controller(method, function, pattern, bases, authenticated=False):
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
    return type(name, parents, {function_name: function, 'requires_authentication': authenticated})


def make_responder(method, bases1=()):
    def responder(pattern, authenticated=False, bases2=()):
        def dec(func):
            bases = tuple(bases1) + tuple(bases2)
            ctrl = make_controller(method, func, pattern, bases, authenticated=authenticated)
            routes.append((pattern, ctrl))

            return func
        return dec
    return responder


def mount_responder_factory(obj, bases=()):
    for method in HTTP_METHODS:
        setattr(obj, method, make_responder(method, bases))

    return obj

mount_responder_factory(self)
