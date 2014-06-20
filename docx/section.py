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

    @property
    def start_type(self):
        """
        The member of the ``WD_SECTION`` enumeration corresponding to the
        initial break behavior of this section, e.g. ``WD_SECTION.ODD_PAGE``
        if the section should begin on the next odd page.
        """
        return self._sectPr.start_type

    @start_type.setter
    def start_type(self, value):
        self._sectPr.start_type = value
