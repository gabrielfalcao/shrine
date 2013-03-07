#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import traceback

from hashlib import sha1
from shrine.conf import settings

from tornado.web import RequestHandler
from tornado import template
from shrine.log import logger
from shrine.views import widget
from shrine.engine import ControllerLoader
from shrine.models import User


class PrettyErrorRequestHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'text/html')
        if not settings.DEBUG and not settings.FORCE_TRACEBACK:
            self.finish("""<h1>Server Error</h1>""")

        if "exc_info" in kwargs:
            exc_info = kwargs["exc_info"]
            trace_info = ''.join(["%s<br/>" % line for line in traceback.format_exception(*exc_info)])
            request_info = ''.join(["<strong>%s</strong>: <code>%s</code> <br /> <hr />" % (k, self.request.__dict__[k]) for k in self.request.__dict__.keys()])
            error = exc_info[1]
            self.finish('''<html>
                            <head>
                             <title>%s</title>
                             <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                             </head>
                             <body>
                                <style type="text/css">
                                * {font-family: Helvetica, Arial, sans-serif;}
                                code {font-family: Monaco, monospace; width: 100%%; max-height: 300px;overflow:auto; }
                                code.block {background-color: #EEE; border: 2px solid #444; overflow:scroll;display:block;}
                                </style>
                                <h2>Error</h2>
                                <p>%s</p>
                                <h2>Traceback</h2>
                                <code class="block">%s</code>
                                <h2>Request Info</h2>
                                <p>%s</p>
                             </body>
                           </html>''' % (error, error,
                                        trace_info, request_info))


class SessionRequestHandler(PrettyErrorRequestHandler):
    user_id_cookie_key = 'user_id'
    _user = None
    session = None
    requires_authentication = False
    session_key = None

    def prepare(self):
        self.action = self.Actor(self)
        self.requires_authentication = any([
            self.requires_authentication,
            self.action.requires_authentication
        ])

    def authenticate(self, user, redirect=True):
        self.session[self.user_id_cookie_key] = user.id
        self.session.modified = True
        self.session.save()

        if redirect:
            return self.redirect(self.get_argument('next', settings.AUTHENTICATED_HOME))

    def get_error_html(self, status_code, *args, **kw):
        tb = traceback.format_exc()
        logger.error(
            u'caught a %s while on "%s"\n\n',
            str(status_code),
            tb,
        )
        return tb

    def logout(self, redirect=True):
        self.session.flush()
        self.session.save()
        self.clear_all_cookies()
        if redirect:
            self.redirect(settings.ANONYMOUS_HOME)

    @property
    def user_id(self):
        uid = self.session.get(self.user_id_cookie_key)
        return int(uid or 0)

    @property
    def user(self):
        if self.user_id:
            try:
                usr = User.objects.get(id=self.user_id)
                return usr
            except User.DoesNotExist:
                return

        return

    def generate_session_key(self):
        shahash = sha1()
        shahash.update(str(time.time()))
        shahash.update(self.request.remote_ip)
        h = shahash.hexdigest()
        return h

    def get_context(self):
        user = self.user
        context = dict(
            settings=settings,
            user=user,
            session=self.session,
            widget=widget.collection(),
        )
        return context

    def render(self, name, **context):
        ControllerLoader(settings.WORKING_DIR).seek_and_destroy()
        ctx = context.copy()
        ctx.update(self.get_context())
        loader = template.Loader(settings.TEMPLATE_PATH)
        self.write(loader.load(name).generate(**ctx))

    def get_normalized_params(self):
        params = self.request.arguments
        return dict([(k, self.get_argument(k)) for k in params])

    def finish(self, *args, **kw):
        if self.session_key:
            self.set_secure_cookie(settings.SESSION_COOKIE_NAME,
                                   self.session_key)

        return super(SessionRequestHandler, self).finish(*args, **kw)
