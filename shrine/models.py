#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth import get_user_model


class ORM(object):
    def __init__(self):
        for app in models.get_apps():
            appname = app.__name__.split('.')[0]
            setattr(self, appname, app)

        for Model in models.get_models():
            setattr(self, Model.__name__, Model)


orm = ORM()

User = get_user_model()
