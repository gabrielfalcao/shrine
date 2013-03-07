#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import couleur
from shrine.controllers import SessionRequestHandler
from shrine.routes import routes

from django.utils.importlib import import_module

from shrine.conf import settings
self = sys.modules[__name__]

HTTP_METHODS = ['get', 'post', 'put', 'delete', 'head', 'options', 'patch']


def method_color(method):
    return {
        'get': '\033[1;32m',
        'post': '\033[1;33m',
        'delete': '\033[1;31m',
        'put': '\033[1;36m',
        'options': '\033[0;37m',
        'head': '\033[1;34m',
        'patch': '\033[1;35m',
    }[method.lower()]

sh = couleur.Shell()


class Actor(object):
    requires_authentication = False

    def __init__(self, controller):
        self.controller = controller
        self.requires_authentication = (
            self.requires_authentication or
            controller.requires_authentication)

    def handle_anonymous(self, method, *args, **kwargs):
        self.controller.set_status(401)
        return self.controller.render("401.html")


class Controller(SessionRequestHandler):
    Actor = Actor

    def get_or_create_session(self):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = self.get_secure_cookie(
            settings.SESSION_COOKIE_NAME)

        self.session = engine.SessionStore(session_key=session_key)
        self.session_key = session_key or self.generate_session_key()
        try:
            self.session.save()
        except Exception:
            # TODO check this marreta
            pass

    def perform(self, method, args, kwargs):
        self.get_or_create_session()
        if self.requires_authentication and not self.user:
            return self.action.handle_anonymous(method, *args, **kwargs)

        responder = getattr(self, 'do_{0}'.format(method))
        sh.bold_white("{method_color}[{method}] {path}\033[0m\n".format(
            method=method.upper(),
            method_color=method_color(method),
            path=self.request.path)
        )

        retval = responder(*args, **kwargs)
        if self.session_key:
            self.set_secure_cookie(settings.SESSION_COOKIE_NAME,
                                   self.session_key)
            self.session.save()

        return retval

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


def make_controller(method, function, pattern, bases, authenticated=False, actor=None):
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
    attributes = {
        function_name: function,
        'requires_authentication': authenticated
    }
    if actor:
        attributes['Actor'] = actor

    return type(name, parents, attributes)


def make_responder(method, bases1=()):
    def responder(pattern, authenticated=False, actor=None, bases2=()):
        def dec(func):
            bases = tuple(bases1) + tuple(bases2)
            ctrl = make_controller(method, func, pattern, bases, authenticated=authenticated, actor=actor)
            routes.append((pattern, ctrl))

            return func
        return dec
    return responder


def mount_responder_factory(obj, bases=()):
    for method in HTTP_METHODS:
        setattr(obj, method, make_responder(method, bases))

    return obj

mount_responder_factory(self)
