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

from __future__ import print_function

try:
    import argcomplete
except ImportError:
    argcomplete = None

import argparse
from collections import namedtuple
from contextlib import contextmanager

try:
    from coverage import coverage
except ImportError:
    coverage = None

try:
    from flake8.engine import get_style_guide
    from flake8.main import print_report
    flake8_installed = True
except ImportError:
    flake8_installed = False

import os

try:
    import pep257
except ImportError:
    pep257 = None

# Don't import sphinx_inventory here or else it will interfere with the code
# coverage results
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(BASE_DIR, 'sphinx_inventory')
TESTS_DIR = os.path.join(CODE_DIR, 'tests')


def parse_args(prog, args):
    parser = argparse.ArgumentParser(prog)
    parser.add_argument('--no-checks', dest='checks', default=flake8_installed,
                        action='store_false', help='Disable static checkers')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Make unittest testrunner verbose')
    parser.add_argument('--no-tests', dest='unittests', default=True,
                        action='store_false',
                        help='Disable running the testsuite')
    parser.add_argument('--run-coverage', action='store_true', default=False,
                        help='Run coverage.py on the testsuite')
    if argcomplete:
        argcomplete.autocomplete(parser)
    return parser.parse_args(args)


@contextmanager
def code_coverage(args):
    if args.run_coverage and coverage:
        print("Code coverage enabled.")
        cov = coverage(config_file=os.path.join(BASE_DIR, '.coveragerc'))
        cov.start()

    try:
        yield
    finally:
        if args.run_coverage and coverage:
            cov.stop()
            cov.report()


def run_flake8():
    print('Running flake8...')
    flake8 = get_style_guide(exclude=['.tox', 'build'], max_complexity=10)
    report = flake8.check_files([BASE_DIR])

    return print_report(report, flake8)


def run_pep257():
    print('Running pep257...')
    pep257_options = namedtuple('PEP257Options', [
        'explain',
        'source',
        'ignore',
        'match',
        'match_dir',
    ])
    # Default options in the option parser
    options = pep257_options(False, False, '', '(?!test_).*\.py', '[^\.].*')
    return pep257.main(options, [CODE_DIR])


def run_unit_tests(args, verbosity):
    print('Running unit tests...')
    with code_coverage(args):
        suite = unittest.TestLoader().discover(TESTS_DIR,
                                               top_level_dir=BASE_DIR)
        result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
        if result.wasSuccessful():
            return 0
        else:
            return 1


def main(argv):
    args = parse_args(argv[0], argv[1:])

    verbosity = 1
    if args.verbose:
        verbosity += 1

    runners = []

    if args.checks:
        if flake8_installed:
            runners.append(run_flake8)
        if pep257:
            runners.append(run_pep257)
    if args.unittests:
        runners.append(lambda: run_unit_tests(args, verbosity))

    for runner in runners:
        exit_code = runner()
        if exit_code > 0:
            return exit_code

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
