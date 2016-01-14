# encoding: utf-8

"""
Shading-related proxy types.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from .mixins.PrMixin import PrMixin
from docx.shared import ElementProxy


class Shd(PrMixin, ElementProxy):
    """
    Proxy object wrapping ``<w:shd>`` element.
    """

    def _get_shdading_node(self):
        pr = self._get_pr_node()

        if pr is not None:
            shd = pr.shd
        else:
            shd = None

        return shd

    def _get_or_add_shading_node(self):
        return self._get_or_add_pr_node().get_or_add_shd()

    @property
    def color(self):
        return self._get_prop('color')

    @color.setter
    def color(self, value):
        self._set_prop('color', value)

    @property
    def fill(self):
        return self._get_prop('fill')

    @fill.setter
    def fill(self, value):
        self._set_prop('fill', value)

    @property
    def themeColor(self):
        return self._get_prop('themeColor')

    @themeColor.setter
    def themeColor(self, value):
        self._set_prop('themeColor', value)

    @property
    def themeFill(self):
        return self._get_prop('themeFill')

    @themeFill.setter
    def themeFill(self, value):
        self._set_prop('themeFill', value)

    @property
    def themeFillShade(self):
        return self._get_prop('themeFillShade')

    @themeFillShade.setter
    def themeFillShade(self, value):
        self._set_prop('themeFillShade', value)

    @property
    def themeFillTint(self):
        return self._get_prop('themeFillTint')

    @themeFillTint.setter
    def themeFillTint(self, value):
        self._set_prop('themeFillTint', value)

    @property
    def themeShade(self):
        return self._get_prop('themeShade')

    @themeShade.setter
    def themeShade(self, value):
        self._set_prop('themeShade', value)

    @property
    def themeTint(self):
        return self._get_prop('themeTint')

    @themeTint.setter
    def themeTint(self, value):
        self._set_prop('themeTint', value)

    @property
    def val(self):
        return self._get_prop('val')

    @val.setter
    def val(self, value):
        self._set_prop('val', value)

    def _get_prop(self, name):
        """
        Return the value of boolean child of `w:[r|p|tc|tbl]Pr` having *name*.
        """
        shd = self._get_shdading_node()
        if shd is None:
            return None
        return getattr(shd, name)

    def _set_prop(self, name, value):
        """
        Assign *value* to the boolean child *name* of `w:[r|p|tc|tbl]Pr`.
        """
        shd = self._get_or_add_shading_node()
        setattr(shd, name, value)
