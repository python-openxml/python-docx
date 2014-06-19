# encoding: utf-8

"""
The |Section| object and related proxy classes.
"""

from __future__ import absolute_import, print_function, unicode_literals


class Section(object):
    """
    Document section, providing access to section and page setup settings.
    """
    def __init__(self, sectPr):
        super(Section, self).__init__()
        self._sectPr = sectPr
