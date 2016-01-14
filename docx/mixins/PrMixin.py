# encoding: utf-8

"""
Mixin for common cross-class variable access
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


class PrMixin(object):
    def _get_pr_node(self):
        for v in dir(self._element):
            if v.endswith('Pr') and not callable(getattr(self._element, v)):
                return getattr(self._element, v)
        else:
            raise AttributeError(str(type(self)) + 'has no attribute ".Pr"')

    def _get_or_add_pr_node(self):
        for v in dir(self._element):
            if v.endswith("Pr") and v.startswith("get_or_add") and callable(getattr(self._element, v)):
                methodToCall = getattr(self._element, v)
                return methodToCall()
        else:
            raise AttributeError(str(type(self)) + 'has no attribute ".Pr"')
