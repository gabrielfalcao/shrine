#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shrine import get


@get('/(?P<matched>.*)')
def index(controller, matched):
    controller.render('index.html', dict(matched=matched))
