#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import traceback

from hashlib import sha1
from shrine.conf import settings
from django.utils.importlib import import_module
from django.contrib.auth.models import User
from tornado.web import RequestHandler
from shrine.log import logger


class PrettyErrorRequestHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'text/html')
        if not settings.DEBUG:
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

    def authenticate(self, user, redirect=True):
        self.session[self.user_id_cookie_key] = user.id
        self.session.save()
        if redirect:
            self.redirect(self.get_argument('next', settings.AUTHENTICATED_HOME))

    def get_error_html(self, status_code, *args, **kw):
        tb = traceback.format_exc()
        logger.error(
            u'caught a %s while on "%s"\n\n',
            str(status_code),
            tb,
        )
        return tb

    def logout(self):
        self.session.flush()
        self.clear_all_cookies()
        return self.redirect(settings.ANONYMOUS_HOME)

    def get_current_user(self):
        uid = self.session.get(self.user_id_cookie_key)

        if uid:
            try:
                return User.objects.get(id=uid)
            except User.DoesNotExist:
                pass

    @property
    def user(self):
        if not self._user:
            self._user = self.get_current_user()

        return self._user

    def generate_session_key(self):
        shahash = sha1()
        shahash.update(str(time.time()))
        shahash.update(self.request.remote_ip)
        return shahash.hexdigest()

    def prepare(self):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = self.get_cookie(
            settings.SESSION_COOKIE_NAME, self.generate_session_key())

        self.session = engine.SessionStore(session_key)

    def get_context(self):
        user = self.user
        context = dict(
            settings=settings,
            user=user,
            session=self.session,
        )
        return context

    def render(self, __template, **context):
        context.update(self.get_context())
        return super(SessionRequestHandler, self).render(__template, **context)

    def get_normalized_params(self):
        params = self.request.arguments
        return dict([(k, self.get_argument(k)) for k in params])

    def finish(self, *args, **kw):
        if self.session:
            self.set_cookie(settings.SESSION_COOKIE_NAME,
                            self.session.session_key)

        super(SessionRequestHandler, self).finish(*args, **kw)
