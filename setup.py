#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup


def get_packages():
    packages = []
    for root, dirnames, filenames in os.walk('shrine'):
        if '__init__.py' in filenames:
            packages.append(".".join(os.path.split(root)).strip("."))

    return packages

required_modules = [
    'tornado',
    'django',
    'sure',
    'lettuce',
    'httpretty',
    'virtualenvwrapper',
    'requests',
    'dj_database_url',
    'envoy',
    'south',
    'couleur',
]

setup(
    name='shrine',
    version='0.0.1',
    description='Tornado + Django',
    author=u'Gabriel Falcao',
    author_email='gabriel@nacaolivre.org',
    url='http://falcao.it/shrine',
    packages=get_packages(),
    install_requires=required_modules,
    entry_points={
        'console_scripts': ['shrine = shrine.bin:main'],
    },
    package_data={
        'shrine': ['COPYING', '*.md'],
    },
)
