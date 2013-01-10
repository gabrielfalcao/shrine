#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.web import Application

routes = [
]


def make_application(**config):
    from shrine.conf import settings
    configuration = {
        'template_path': settings.LOCAL_FILE(settings.TEMPLATE_PATH),
    }
    configuration.update(config)

    return Application(routes, **configuration)
