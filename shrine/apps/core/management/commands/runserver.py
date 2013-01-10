#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from django.core.management.commands.runserver import Command as BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        os.system('shrine run')
