# encoding: utf-8

"""
Provides Python 2/3 compatibility objects
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

# ===========================================================================
# Python 3 versions
# ===========================================================================

if sys.version_info >= (3, 0):

    from collections.abc import Sequence
    from io import BytesIO

    def is_string(obj):
        """Return True if *obj* is a string, False otherwise."""
        return isinstance(obj, str)

    Unicode = str

# ===========================================================================
# Python 2 versions
# ===========================================================================

else:

    from collections import Sequence  # noqa
    from StringIO import StringIO as BytesIO  # noqa

    def is_string(obj):
        """Return True if *obj* is a string, False otherwise."""
        return isinstance(obj, basestring)  # noqa

    Unicode = unicode  # noqa
