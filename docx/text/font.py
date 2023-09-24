# encoding: utf-8

"""
Font-related proxy objects.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from ..dml.color import ColorFormat
from ..shared import ElementProxy


class Font(ElementProxy):
    """
    Proxy object wrapping the parent of a ``<w:rPr>`` element and providing
    access to character properties such as font name, font size, bold, and
    subscript.
    """

    __slots__ = ()

    @property
    def all_caps(self):
        """
        Read/write. Causes text in this font to appear in capital letters.
        """
        return self._get_bool_prop("caps")

    @all_caps.setter
    def all_caps(self, value):
        self._set_bool_prop("caps", value)

    @property
    def bold(self):
        """
        Read/write. Causes text in this font to appear in bold.
        """
        return self._get_bool_prop("b")

    @bold.setter
    def bold(self, value):
        self._set_bool_prop("b", value)

    @property
    def color(self):
        """
        A |ColorFormat| object providing a way to get and set the text color
        for this font.
        """
        return ColorFormat(self._element)

    @property
    def complex_script(self):
        """
        Read/write tri-state value. When |True|, causes the characters in the
        run to be treated as complex script regardless of their Unicode
        values.
        """
        return self._get_bool_prop("cs")

    @complex_script.setter
    def complex_script(self, value):
        self._set_bool_prop("cs", value)

    @property
    def cs_bold(self):
        """
        Read/write tri-state value. When |True|, causes the complex script
        characters in the run to be displayed in bold typeface.
        """
        return self._get_bool_prop("bCs")

    @cs_bold.setter
    def cs_bold(self, value):
        self._set_bool_prop("bCs", value)

    @property
    def cs_italic(self):
        """
        Read/write tri-state value. When |True|, causes the complex script
        characters in the run to be displayed in italic typeface.
        """
        return self._get_bool_prop("iCs")

    @cs_italic.setter
    def cs_italic(self, value):
        self._set_bool_prop("iCs", value)

    @property
    def double_strike(self):
        """
        Read/write tri-state value. When |True|, causes the text in the run
        to appear with double strikethrough.
        """
        return self._get_bool_prop("dstrike")

    @double_strike.setter
    def double_strike(self, value):
        self._set_bool_prop("dstrike", value)

    @property
    def emboss(self):
        """
        Read/write tri-state value. When |True|, causes the text in the run
        to appear as if raised off the page in relief.
        """
        return self._get_bool_prop("emboss")

    @emboss.setter
    def emboss(self, value):
        self._set_bool_prop("emboss", value)

    @property
    def hidden(self):
        """
        Read/write tri-state value. When |True|, causes the text in the run
        to be hidden from display, unless applications settings force hidden
        text to be shown.
        """
        return self._get_bool_prop("vanish")

    @hidden.setter
    def hidden(self, value):
        self._set_bool_prop("vanish", value)

    @property
    def highlight_color(self):
        """
        A member of :ref:`WdColorIndex` indicating the color of highlighting
        applied, or `None` if no highlighting is applied.
        """
        rPr = self._element.rPr
        if rPr is None:
            return None
        return rPr.highlight_val

    @highlight_color.setter
    def highlight_color(self, value):
        rPr = self._element.get_or_add_rPr()
        rPr.highlight_val = value

    @property
    def italic(self):
        """
        Read/write tri-state value. When |True|, causes the text of the run
        to appear in italics. |None| indicates the effective value is
        inherited from the style hierarchy.
        """
        return self._get_bool_prop("i")

    @italic.setter
    def italic(self, value):
        self._set_bool_prop("i", value)

    @property
    def imprint(self):
        """
        Read/write tri-state value. When |True|, causes the text in the run
        to appear as if pressed into the page.
        """
        return self._get_bool_prop("imprint")

    @imprint.setter
    def imprint(self, value):
        self._set_bool_prop("imprint", value)

    @property
    def math(self):
        """
        Read/write tri-state value. When |True|, specifies this run contains
        WML that should be handled as though it was Office Open XML Math.
        """
        return self._get_bool_prop("oMath")

    @math.setter
    def math(self, value):
        self._set_bool_prop("oMath", value)

    @property
    def name(self):
        """
        Get or set the typeface name for this |Font| instance, causing the
        text it controls to appear in the named font, if a matching font is
        found. |None| indicates the typeface is inherited from the style
        hierarchy.
        """
        rPr = self._element.rPr
        if rPr is None:
            return None
        return rPr.rFonts_ascii

    @name.setter
    def name(self, value):
        rPr = self._element.get_or_add_rPr()
        rPr.rFonts_ascii = value
        rPr.rFonts_hAnsi = value

    @property
    def no_proof(self):
        """
        Read/write tri-state value. When |True|, specifies that the contents
        of this run should not report any errors when the document is scanned
        for spelling and grammar.
        """
        return self._get_bool_prop("noProof")

    @no_proof.setter
    def no_proof(self, value):
        self._set_bool_prop("noProof", value)

    @property
    def outline(self):
        """
        Read/write tri-state value. When |True| causes the characters in the
        run to appear as if they have an outline, by drawing a one pixel wide
        border around the inside and outside borders of each character glyph.
        """
        return self._get_bool_prop("outline")

    @outline.setter
    def outline(self, value):
        self._set_bool_prop("outline", value)

    @property
    def rtl(self):
        """
        Read/write tri-state value. When |True| causes the text in the run
        to have right-to-left characteristics.
        """
        return self._get_bool_prop("rtl")

    @rtl.setter
    def rtl(self, value):
        self._set_bool_prop("rtl", value)

    @property
    def shadow(self):
        """
        Read/write tri-state value. When |True| causes the text in the run
        to appear as if each character has a shadow.
        """
        return self._get_bool_prop("shadow")

    @shadow.setter
    def shadow(self, value):
        self._set_bool_prop("shadow", value)

    @property
    def size(self):
        """
        Read/write |Length| value or |None|, indicating the font height in
        English Metric Units (EMU). |None| indicates the font size should be
        inherited from the style hierarchy. |Length| is a subclass of |int|
        having properties for convenient conversion into points or other
        length units. The :class:`docx.shared.Pt` class allows convenient
        specification of point values::

            >> font.size = Pt(24)
            >> font.size
            304800
            >> font.size.pt
            24.0
        """
        rPr = self._element.rPr
        if rPr is None:
            return None
        return rPr.sz_val

    @size.setter
    def size(self, emu):
        rPr = self._element.get_or_add_rPr()
        rPr.sz_val = emu

    @property
    def small_caps(self):
        """
        Read/write tri-state value. When |True| causes the lowercase
        characters in the run to appear as capital letters two points smaller
        than the font size specified for the run.
        """
        return self._get_bool_prop("smallCaps")

    @small_caps.setter
    def small_caps(self, value):
        self._set_bool_prop("smallCaps", value)

    @property
    def snap_to_grid(self):
        """
        Read/write tri-state value. When |True| causes the run to use the
        document grid characters per line settings defined in the docGrid
        element when laying out the characters in this run.
        """
        return self._get_bool_prop("snapToGrid")

    @snap_to_grid.setter
    def snap_to_grid(self, value):
        self._set_bool_prop("snapToGrid", value)

    @property
    def spec_vanish(self):
        """
        Read/write tri-state value. When |True|, specifies that the given run
        shall always behave as if it is hidden, even when hidden text is
        being displayed in the current document. The property has a very
        narrow, specialized use related to the table of contents. Consult the
        spec (§17.3.2.36) for more details.
        """
        return self._get_bool_prop("specVanish")

    @spec_vanish.setter
    def spec_vanish(self, value):
        self._set_bool_prop("specVanish", value)

    @property
    def strike(self):
        """
        Read/write tri-state value. When |True| causes the text in the run
        to appear with a single horizontal line through the center of the
        line.
        """
        return self._get_bool_prop("strike")

    @strike.setter
    def strike(self, value):
        self._set_bool_prop("strike", value)

    @property
    def subscript(self):
        """
        Boolean indicating whether the characters in this |Font| appear as
        subscript. |None| indicates the subscript/subscript value is
        inherited from the style hierarchy.
        """
        rPr = self._element.rPr
        if rPr is None:
            return None
        return rPr.subscript

    @subscript.setter
    def subscript(self, value):
        rPr = self._element.get_or_add_rPr()
        rPr.subscript = value

    @property
    def superscript(self):
        """
        Boolean indicating whether the characters in this |Font| appear as
        superscript. |None| indicates the subscript/superscript value is
        inherited from the style hierarchy.
        """
        rPr = self._element.rPr
        if rPr is None:
            return None
        return rPr.superscript

    @superscript.setter
    def superscript(self, value):
        rPr = self._element.get_or_add_rPr()
        rPr.superscript = value

    @property
    def underline(self):
        """
        The underline style for this |Font|, one of |None|, |True|, |False|,
        or a value from :ref:`WdUnderline`. |None| indicates the font
        inherits its underline value from the style hierarchy. |False|
        indicates no underline. |True| indicates single underline. The values
        from :ref:`WdUnderline` are used to specify other outline styles such
        as double, wavy, and dotted.
        """
        rPr = self._element.rPr
        if rPr is None:
            return None
        return rPr.u_val

    @underline.setter
    def underline(self, value):
        rPr = self._element.get_or_add_rPr()
        rPr.u_val = value

    @property
    def web_hidden(self):
        """
        Read/write tri-state value. When |True|, specifies that the contents
        of this run shall be hidden when the document is displayed in web
        page view.
        """
        return self._get_bool_prop("webHidden")

    @web_hidden.setter
    def web_hidden(self, value):
        self._set_bool_prop("webHidden", value)

    def _get_bool_prop(self, name):
        """
        Return the value of boolean child of `w:rPr` having *name*.
        """
        rPr = self._element.rPr
        if rPr is None:
            return None
        return rPr._get_bool_val(name)

    def _set_bool_prop(self, name, value):
        """
        Assign *value* to the boolean child *name* of `w:rPr`.
        """
        rPr = self._element.get_or_add_rPr()
        rPr._set_bool_val(name, value)
