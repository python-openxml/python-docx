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
    def page_height(self):
        """
        Total page height used for this section, inclusive of all edge spacing
        values such as margins. Page orientation is taken into account, so
        for example, its expected value would be ``Inches(8.5)`` for
        letter-sized paper when orientation is landscape.
        """
        return self._sectPr.page_height

    @property
    def page_width(self):
        """
        Total page width used for this section, inclusive of all edge spacing
        values such as margins. Page orientation is taken into account, so
        for example, its expected value would be ``Inches(11)`` for
        letter-sized paper when orientation is landscape.
        """
        return self._sectPr.page_width

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
