"""Objects related to shading."""


from __future__ import absolute_import, division, print_function, unicode_literals

from docx.shared import ElementProxy


class Shading(ElementProxy):
    """
    A shading object defining the shading properties of a table cell or document paragraph.
    """

    __slots__ = "_shd"

    def __init__(self, element):
        super(Shading, self).__init__(element, None)
        self._shd = element

    @property
    def background_pattern_color(self):
        """Return background color of selected element."""
        return self._shd.color

    @background_pattern_color.setter
    def background_pattern_color(self, value):
        """Set background color of selected element."""
        self._shd.color = value

    @property
    def foreground_pattern_color(self):
        """Return the color of the applied texture."""
        return self._shd.fill

    @foreground_pattern_color.setter
    def foreground_pattern_color(self, value):
        """Set the color of the applied texture."""
        self._shd.fill = value

    @property
    def texture(self):
        """Return texture of shaded element.
        By default the value is set to 'clear'.
        """
        return self._shd.val

    @texture.setter
    def texture(self, value):
        self._shd.val = value
