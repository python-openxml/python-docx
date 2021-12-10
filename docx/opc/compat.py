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

    def cls_method_fn(cls, method_name):
        """
        Return the function object associated with the method of *cls* having
        *method_name*.
        """
        return getattr(cls, method_name)

    def is_string(obj):
        """
        Return True if *obj* is a string, False otherwise.
        """
        return isinstance(obj, str)


# ===========================================================================
# Python 2 versions
# ===========================================================================

else:

    def cls_method_fn(cls, method_name):
        """
        Return the function object associated with the method of *cls* having
        *method_name*.
        """
        unbound_method = getattr(cls, method_name)
        return unbound_method.__func__

    def is_string(obj):
        """
        Return True if *obj* is a string, False otherwise.
        """
        return isinstance(obj, basestring)  # noqa
