# -*- coding: utf-8 -*-
#
# Copyright 2014 Mark Lee
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
#
# Parts are based on examining Sphinx's source code, specifically
# sphinx.builders.html.StandaloneHTMLBuilder.dump_inventory(), which is
# Copyright 2007-2014 by the Sphinx team, under the BSD (2-clause) license.
"""Inventory writer."""

from __future__ import unicode_literals

import zlib
from ._compat import items


class Inventory(object):

    """Writes a Sphinx inventory (version 2)."""

    def __init__(self, project, version):
        """
        Create the object.

        :param bytes project: The project name (UTF-8 encoded)
        :param bytes version: The project version (UTF-8 encoded)
        """
        self.project = project
        self.version = version

    def preamble(self):
        """
        Generate the format's preamble.

        :rtype: bytes
        """
        return '''\
# Sphinx inventory version 2
# Project: {project}
# Version: {version}
# The remainder of this file is compressed using zlib.
'''.format(project=self.project, version=self.version).encode('utf-8')

    def write(self, domain, refs, inventory_filename):
        """Write the Sphinx inventory file."""
        with open(inventory_filename, 'wb') as f:
            f.write(self.preamble())
            compressor = zlib.compressobj(9)
            fmt = '{name} {domain}:{ref_type} {priority} {uri} {dispname}\n'
            # I'm not quite sure what priority does (if anything).
            priority = '1'
            dispname = '-'
            for ref_type, metadata in items(refs):
                for name, uri in items(metadata):
                    inv_item = fmt.format(**locals()).encode('utf-8')
                    f.write(compressor.compress(inv_item))
            f.write(compressor.flush())
