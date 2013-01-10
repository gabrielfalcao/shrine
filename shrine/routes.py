#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.web import Application, StaticFileHandler

routes = [
]


def make_application(**config):
    from shrine.conf import settings

    static_path = settings.LOCAL_FILE(settings.STATIC_PATH)
    configuration = {
        'template_path': settings.LOCAL_FILE(settings.TEMPLATE_PATH),
    }
    configuration.update(config)
    routes.append((r"/media/(.*)", StaticFileHandler, {"path": static_path}))
    return Application(routes, **configuration)
