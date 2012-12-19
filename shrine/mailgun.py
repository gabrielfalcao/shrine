#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger('email')


class EmailBackend(BaseEmailBackend):
    def send_through_mailgun(self, msg):
        url = "https://api.mailgun.net/v2/{0}/messages".format(
            settings.MAILGUN_SERVER_NAME)

        html = msg.body
        if msg.alternatives:
            html = msg.alternatives[0][0]

        r = (requests.post(
            url,
            auth=("api", settings.MAILGUN_ACCESS_KEY),
            data={
                "from": msg.from_email,
                "to": msg.recipients(),
                "subject": msg.subject,
                "text": msg.body,
                "html": html,
            }))
        logger.info('Email sent to mailgun: %r', r)

        return msg

    def send_messages(self, email_messages):
        return map(self.send_through_mailgun, email_messages)
