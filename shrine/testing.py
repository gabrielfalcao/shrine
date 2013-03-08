#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import socket

from functools import wraps

from multiprocessing import Process
from shrine.cmds.run import RunProject
from urlparse import urljoin


class RunTestServer(RunProject):
    def get_settings(self):
        return type('shrine.testing.settings', (), {
            'PORT': 9000,
            'PRODUCT_NAME': 'Test server',
        })


class ShrineTestServer(object):
    def __init__(self, process, logfile, host, port):
        self.process = process
        self.logfile = logfile
        self.host = host
        self.port = port

    @property
    def address(self):
        return 'http://{0}:{1}'.format(self.host, self.port)

    def url(self, path):
        return urljoin(self.address, path)


def server_up(address, port):
    s = socket.socket()
    try:
        s.connect((address, port))
        return True
    except socket.error:
        return False


def wait_server(host, port, timeout):
    if timeout < 0:
        return

    for attempt in range(int(timeout * 100)):
        if server_up(host, port):
            break

        time.sleep(timeout / 10.0)

    if not server_up(host, port):
        msg = "could not run the server on {host}:{port}".format(**locals())
        raise RuntimeError(msg)


def runserver(host='localhost', port=9000, logfile=None):
    with open(logfile, 'w') as output:
        sys.stderr = output
        sys.stdout = output
        RunTestServer(output).run([])
        output.flush()


def tornado_server(port=9000, host='localhost', wait=0.5):
    def decorator(func):
        logfile = 'shrine.test.log'

        @wraps(func)
        def wrapper(*args, **kw):
            p = Process(target=runserver, kwargs={'port': int(port), 'host': host, 'logfile': logfile})
            server = ShrineTestServer(p, logfile=logfile, host=host, port=port)

            p.start()
            wait_server(host, port, wait)
            try:
                retval = func(server, *args, **kw)
            finally:
                os.kill(p.pid, 9)

            return retval

        return wrapper

    if callable(port):
        func = port
        port = 9000

        return decorator(func)

    return decorator
