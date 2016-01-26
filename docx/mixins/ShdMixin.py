# encoding: utf-8

"""
Mixin for shared functions applying to all related objects.  To be used for rPr, pPr, tbl, and tcPr tags.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..shading import Shd
from ..mixins.PrMixin import PrMixin


class ShdMixin(PrMixin, object):
    @property
    def shd(self):
        return Shd(self._element)

    @property
    def shd_val(self):
        """
        The value of `w:shd/@w:val`.
        """
        shd = self.shd
        return shd.val

    @shd_val.setter
    def shd_val(self, value):
        self.shd.val = value

    @property
    def shd_color(self):
        """
        The value of `w:shd/@w:color`.
        """
        shd = self.shd

        return shd.color

    @shd_color.setter
    def shd_color(self, value):
        self.shd.color = value

    @property
    def shd_fill(self):
        """
        The value of `w:shd/@w:fill`.
        """
        shd = self.shd
        return shd.fill

    @shd_fill.setter
    def shd_fill(self, value):
        self.shd.fill = value

    @property
    def shd_themeColor(self):
        """
        The value of `w:shd/@w:themeColor`.
        """
        shd = self.shd
        return shd.themeColor

    @shd_themeColor.setter
    def shd_themeColor(self, value):
        self.shd.themeColor = value

    @property
    def shd_themeFill(self):
        """
        The value of `w:shd/@w:themeFill`.
        """
        shd = self.shd
        return shd.themeFill

    @shd_themeFill.setter
    def shd_themeFill(self, value):
        self.shd.themeFill = value

    @property
    def shd_themeFillShade(self):
        """
        The value of `w:shd/@w:themeFillShade`.
        """
        shd = self.shd
        return shd.themeFillShade

    @shd_themeFillShade.setter
    def shd_themeFillShade(self, value):
        self.shd.themeFillShade = value

    @property
    def shd_themeFillTint(self):
        """
        The value of `w:shd/@w:themeFillTint`.
        """
        shd = self.shd
        return shd.themeFillTint

    @shd_themeFillTint.setter
    def shd_themeFillTint(self, value):
        self.shd.themeFillTint = value

    @property
    def shd_themeShade(self):
        """
        The value of `w:shd/@w:themeShade`.
        """
        shd = self.shd
        return shd.themeShade

    @shd_themeShade.setter
    def shd_themeShade(self, value):
        self.shd.themeShade = value

    @property
    def shd_themeTint(self):
        """
        The value of `w:shd/@w:themeTint`.
        """
        shd = self.shd
        return shd.themeTint

    @shd_themeTint.setter
    def shd_themeTint(self, value):
        self.shd.themeTint = value
