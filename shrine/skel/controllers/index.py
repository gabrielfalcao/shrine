#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shrine.web import get


@get('/')
def index(controller, *args, **kw):
    controller.render('index.html')
