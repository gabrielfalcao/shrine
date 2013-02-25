#!/usr/bin/env python
# -*- coding: utf-8 -*-


class widget(object):
    registry = {}

    @classmethod
    def register(cls, func):
        cls.registry[func.__name__] = func

    @classmethod
    def collection(cls):
        name = 'WidgetCollection(%s)' % ", ".join(cls.registry.keys())
        collection = type(name, (dict, ), {})(cls.registry)
        for name in cls.registry:
            setattr(collection, name, cls.registry[name])

        return collection


class DomMaker(object):
    def __getattr__(self, name):
        return Tag(name)


class Tag(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, attrs, content):
        long_attrs = " ".join(['%s="%s"' % (k, attrs[k]) for k in attrs])
        ctx = {
            'name': self.name.strip(),
            'attrs': long_attrs and " " + long_attrs or "",
            'content': content,
        }

        if content:
            return '<{name}{attrs}>{content}</{name}>'.format(**ctx)
        else:
            return '<{name}{attrs} />'.format(**ctx)

tag = DomMaker()
