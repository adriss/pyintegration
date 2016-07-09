#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import codecs
import os
import sys

from setuptools import setup


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()

install_requires = [
    'pykka == 1.2.1'
]

tests_require = [
    'pytest',
]


if sys.version_info[:2] < (3, 4):
    tests_require.append('mock >= 1.0.1')
    install_requires.append('enum34 >= 1.0.4, < 2')

setup(
    name='PyIntegration',
    version='1.0',
    description='Enterprise Integration Patterns for Python',
    url='https://www.jccarrillo.com/',
    author='JC Carrillo.',
    packages=['pyintegration'],
    license='Apache License 2.0',
    include_package_data=True,
    test_suite='nose.collector',
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 1 - Development',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
