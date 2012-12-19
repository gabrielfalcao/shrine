#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

from shrine.conf import settings
from shrine.log import logger

MESSAGE = "{} worker pid %d in {}!".format(
    settings.PRODUCT_NAME,
    settings.ENV_NAME,
)

from shrine.routes import app, wsgi

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

__all__ = ['app', 'wsgi']

if __name__ == "__main__":
    import tornado.netutil
    sockets = tornado.netutil.bind_sockets(settings.PORT)
    tornado.process.fork_processes(0)
    server = HTTPServer(app, xheaders=True)
    server.add_sockets(sockets)

    mainloop = IOLoop.instance()

    print MESSAGE % os.getpid()
    mainloop.start()
