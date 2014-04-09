#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013, 2014 Mark Lee
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

####
# Dirty Monkeypatching Hacks
####

# distutils check ReST + pygments
#
# When the long description contains a code block, the distutils ``check -r``
# will fail because the default options do not include ``syntax_highlight``.
# Monkeypatch ``docutils.frontend.OptionParser`` to provide a default for
# this option.

if 'check' in sys.argv:
    try:
        from docutils.frontend import OptionParser
    except ImportError:
        pass  # docutils isn't installed, ignore
    else:
        OptionParser.settings_defaults['syntax_highlight'] = None

####
# Your regularly scheduled setup file
####

import os
from setuptools import find_packages, setup

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from sphinx_inventory import metadata

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

with open('README.rst') as f:
    long_description = f.read()

setup(name='sphinx-inventory',
      version=metadata.VERSION,
      description=metadata.DESCRIPTION,
      long_description=long_description,
      author='Mark Lee',
      author_email='sphinx+inventory.no.spam@lazymalevolence.com',
      url='https://github.com/malept/sphinx-inventory',
      packages=find_packages(),
      classifiers=CLASSIFIERS)
