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

from sphinx.ext.intersphinx import fetch_inventory
from tempfile import NamedTemporaryFile
from ..inventory import Inventory
from . import unittest


class MockApp(object):
    __slots__ = ['warnings', 'srcdir']

    def __init__(self):
        self.warnings = []
        self.srcdir = None

    @property
    def warning_count(self):
        return len(self.warnings)

    def warn(self, msg):  # pragma: no cover
        self.warnings.append(msg)


class InventoryTest(unittest.TestCase):
    """Test case for the Sphinx inventory writer."""

    def assert_write_success(self, domain, refs):
        with NamedTemporaryFile() as f:
            inv = Inventory(b'InventoryTest', b'0.0')

            inv.write(domain, refs, f.name)
            inv_data = self.assert_fetch_inventory_success(f.name)
            return inv_data

    def assert_fetch_inventory_success(self, filename):
        app = MockApp()
        inv_data = fetch_inventory(app, '', filename)
        self.assertEqual(0, app.warning_count, app.warnings)
        self.assertIsInstance(inv_data, dict)
        return inv_data

    def test_write_empty_success(self):
        inv_data = self.assert_write_success('d', {})
        self.assertEqual(0, len(inv_data))

    def test_write_success(self):
        inv_data = self.assert_write_success('domain', {
            'class': {
                'Class1': 'class1.html',
            }
        })
        self.assertEqual(1, len(inv_data))
