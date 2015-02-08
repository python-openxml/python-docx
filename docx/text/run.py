# encoding: utf-8

"""
Run-related proxy objects for python-docx, Run in particular.
"""

from __future__ import absolute_import, print_function, unicode_literals

from ..enum.style import WD_STYLE_TYPE
from ..enum.text import WD_BREAK
from ..shared import ElementProxy, Parented


class Run(Parented):
    """
    Proxy object wrapping ``<w:r>`` element. Several of the properties on Run
    take a tri-state value, |True|, |False|, or |None|. |True| and |False|
    correspond to on and off respectively. |None| indicates the property is
    not specified directly on the run and its effective value is taken from
    the style hierarchy.
    """
    def __init__(self, r, parent):
        super(Run, self).__init__(parent)
        self._r = self._element = self.element = r

    def add_break(self, break_type=WD_BREAK.LINE):
        """
        Add a break element of *break_type* to this run. *break_type* can
        take the values `WD_BREAK.LINE`, `WD_BREAK.PAGE`, and
        `WD_BREAK.COLUMN` where `WD_BREAK` is imported from `docx.enum.text`.
        *break_type* defaults to `WD_BREAK.LINE`.
        """
        type_, clear = {
            WD_BREAK.LINE:             (None,           None),
            WD_BREAK.PAGE:             ('page',         None),
            WD_BREAK.COLUMN:           ('column',       None),
            WD_BREAK.LINE_CLEAR_LEFT:  ('textWrapping', 'left'),
            WD_BREAK.LINE_CLEAR_RIGHT: ('textWrapping', 'right'),
            WD_BREAK.LINE_CLEAR_ALL:   ('textWrapping', 'all'),
        }[break_type]
        br = self._r.add_br()
        if type_ is not None:
            br.type = type_
        if clear is not None:
            br.clear = clear

    def add_picture(self, image_path_or_stream, width=None, height=None):
        """
        Return an |InlineShape| instance containing the image identified by
        *image_path_or_stream*, added to the end of this run.
        *image_path_or_stream* can be a path (a string) or a file-like object
        containing a binary image. If neither width nor height is specified,
        the picture appears at its native size. If only one is specified, it
        is used to compute a scaling factor that is then applied to the
        unspecified dimension, preserving the aspect ratio of the image. The
        native size of the picture is calculated using the dots-per-inch
        (dpi) value specified in the image file, defaulting to 72 dpi if no
        value is specified, as is often the case.
        """
        inline_shapes = self.part.inline_shapes
        picture = inline_shapes.add_picture(image_path_or_stream, self)

        # scale picture dimensions if width and/or height provided
        if width is not None or height is not None:
            native_width, native_height = picture.width, picture.height
            if width is None:
                scaling_factor = float(height) / float(native_height)
                width = int(round(native_width * scaling_factor))
            elif height is None:
                scaling_factor = float(width) / float(native_width)
                height = int(round(native_height * scaling_factor))
            # set picture to scaled dimensions
            picture.width = width
            picture.height = height

        return picture

    def add_tab(self):
        """
        Add a ``<w:tab/>`` element at the end of the run, which Word
        interprets as a tab character.
        """
        self._r._add_tab()

    def add_text(self, text):
        """
        Returns a newly appended |_Text| object (corresponding to a new
        ``<w:t>`` child element) to the run, containing *text*. Compare with
        the possibly more friendly approach of assigning text to the
        :attr:`Run.text` property.
        """
        t = self._r.add_t(text)
        return _Text(t)

    @property
    def bold(self):
        """
        Read/write. Causes the text of the run to appear in bold.
        """
        return self.font.bold

    @bold.setter
    def bold(self, value):
        self.font.bold = value

    def clear(self):
        """
        Return reference to this run after removing all its content. All run
        formatting is preserved.
        """
        self._r.clear_content()
        return self

    @property
    def font(self):
        """
        The |Font| object providing access to the character formatting
        properties for this run, such as font name and size.
        """
        return Font(self._element)

    @property
    def italic(self):
        """
        Read/write tri-state value. When |True|, causes the text of the run
        to appear in italics.
        """
        return self.font.italic

    @italic.setter
    def italic(self, value):
        self.font.italic = value

    @property
    def style(self):
        """
        Read/write. A |_CharacterStyle| object representing the character
        style applied to this run. The default character style for the
        document (often `Default Character Font`) is returned if the run has
        no directly-applied character style. Setting this property to |None|
        removes any directly-applied character style.
        """
        style_id = self._r.style
        return self.part.get_style(style_id, WD_STYLE_TYPE.CHARACTER)

    @style.setter
    def style(self, style_or_name):
        style_id = self.part.get_style_id(
            style_or_name, WD_STYLE_TYPE.CHARACTER
        )
        self._r.style = style_id

    @property
    def text(self):
        """
        String formed by concatenating the text equivalent of each run
        content child element into a Python string. Each ``<w:t>`` element
        adds the text characters it contains. A ``<w:tab/>`` element adds
        a ``\\t`` character. A ``<w:cr/>`` or ``<w:br>`` element each add
        a ``\\n`` character. Note that a ``<w:br>`` element can indicate
        a page break or column break as well as a line break. All ``<w:br>``
        elements translate to a single ``\\n`` character regardless of their
        type. All other content child elements, such as ``<w:drawing>``, are
        ignored.

        Assigning text to this property has the reverse effect, translating
        each ``\\t`` character to a ``<w:tab/>`` element and each ``\\n`` or
        ``\\r`` character to a ``<w:cr/>`` element. Any existing run content
        is replaced. Run formatting is preserved.
        """
        return self._r.text

    @text.setter
    def text(self, text):
        self._r.text = text

    @property
    def underline(self):
        """
        The underline style for this |Run|, one of |None|, |True|, |False|,
        or a value from :ref:`WdUnderline`. A value of |None| indicates the
        run has no directly-applied underline value and so will inherit the
        underline value of its containing paragraph. Assigning |None| to this
        property removes any directly-applied underline value. A value of
        |False| indicates a directly-applied setting of no underline,
        overriding any inherited value. A value of |True| indicates single
        underline. The values from :ref:`WdUnderline` are used to specify
        other outline styles such as double, wavy, and dotted.
        """
        return self.font.underline

    @underline.setter
    def underline(self, value):
        self.font.underline = value


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
        return self._get_bool_prop('caps')

    @all_caps.setter
    def all_caps(self, value):
        self._set_bool_prop('caps', value)

    @property
    def bold(self):
        """
        Read/write. Causes text in this font to appear in bold.
        """
        return self._get_bool_prop('b')

    @bold.setter
    def bold(self, value):
        self._set_bool_prop('b', value)

    @property
    def complex_script(self):
        """
        Read/write tri-state value. When |True|, causes the characters in the
        run to be treated as complex script regardless of their Unicode
        values.
        """
        return self._get_bool_prop('cs')

    @complex_script.setter
    def complex_script(self, value):
        self._set_bool_prop('cs', value)

    @property
    def cs_bold(self):
        """
        Read/write tri-state value. When |True|, causes the complex script
        characters in the run to be displayed in bold typeface.
        """
        return self._get_bool_prop('bCs')

    @cs_bold.setter
    def cs_bold(self, value):
        self._set_bool_prop('bCs', value)

    @property
    def cs_italic(self):
        """
        Read/write tri-state value. When |True|, causes the complex script
        characters in the run to be displayed in italic typeface.
        """
        return self._get_bool_prop('iCs')

    @cs_italic.setter
    def cs_italic(self, value):
        self._set_bool_prop('iCs', value)

    @property
    def double_strike(self):
        """
        Read/write tri-state value. When |True|, causes the text in the run
        to appear with double strikethrough.
        """
        return self._get_bool_prop('dstrike')

    @double_strike.setter
    def double_strike(self, value):
        self._set_bool_prop('dstrike', value)

    @property
    def emboss(self):
        """
        Read/write tri-state value. When |True|, causes the text in the run
        to appear as if raised off the page in relief.
        """
        return self._get_bool_prop('emboss')

    @emboss.setter
    def emboss(self, value):
        self._set_bool_prop('emboss', value)

    @property
    def hidden(self):
        """
        Read/write tri-state value. When |True|, causes the text in the run
        to be hidden from display, unless applications settings force hidden
        text to be shown.
        """
        return self._get_bool_prop('vanish')

    @hidden.setter
    def hidden(self, value):
        self._set_bool_prop('vanish', value)

    @property
    def italic(self):
        """
        Read/write tri-state value. When |True|, causes the text of the run
        to appear in italics. |None| indicates the effective value is
        inherited from the style hierarchy.
        """
        return self._get_bool_prop('i')

    @italic.setter
    def italic(self, value):
        self._set_bool_prop('i', value)

    @property
    def imprint(self):
        """
        Read/write tri-state value. When |True|, causes the text in the run
        to appear as if pressed into the page.
        """
        return self._get_bool_prop('imprint')

    @imprint.setter
    def imprint(self, value):
        self._set_bool_prop('imprint', value)

    @property
    def math(self):
        """
        Read/write tri-state value. When |True|, specifies this run contains
        WML that should be handled as though it was Office Open XML Math.
        """
        return self._get_bool_prop('oMath')

    @math.setter
    def math(self, value):
        self._set_bool_prop('oMath', value)

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
        return self._get_bool_prop('noProof')

    @no_proof.setter
    def no_proof(self, value):
        self._set_bool_prop('noProof', value)

    @property
    def outline(self):
        """
        Read/write tri-state value. When |True| causes the characters in the
        run to appear as if they have an outline, by drawing a one pixel wide
        border around the inside and outside borders of each character glyph.
        """
        return self._get_bool_prop('outline')

    @outline.setter
    def outline(self, value):
        self._set_bool_prop('outline', value)

    @property
    def rtl(self):
        """
        Read/write tri-state value. When |True| causes the text in the run
        to have right-to-left characteristics.
        """
        return self._get_bool_prop('rtl')

    @rtl.setter
    def rtl(self, value):
        self._set_bool_prop('rtl', value)

    @property
    def shadow(self):
        """
        Read/write tri-state value. When |True| causes the text in the run
        to appear as if each character has a shadow.
        """
        return self._get_bool_prop('shadow')

    @shadow.setter
    def shadow(self, value):
        self._set_bool_prop('shadow', value)

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
        return self._get_bool_prop('smallCaps')

    @small_caps.setter
    def small_caps(self, value):
        self._set_bool_prop('smallCaps', value)

    @property
    def snap_to_grid(self):
        """
        Read/write tri-state value. When |True| causes the run to use the
        document grid characters per line settings defined in the docGrid
        element when laying out the characters in this run.
        """
        return self._get_bool_prop('snapToGrid')

    @snap_to_grid.setter
    def snap_to_grid(self, value):
        self._set_bool_prop('snapToGrid', value)

    @property
    def spec_vanish(self):
        """
        Read/write tri-state value. When |True|, specifies that the given run
        shall always behave as if it is hidden, even when hidden text is
        being displayed in the current document. The property has a very
        narrow, specialized use related to the table of contents. Consult the
        spec (§17.3.2.36) for more details.
        """
        return self._get_bool_prop('specVanish')

    @spec_vanish.setter
    def spec_vanish(self, value):
        self._set_bool_prop('specVanish', value)

    @property
    def strike(self):
        """
        Read/write tri-state value. When |True| causes the text in the run
        to appear with a single horizontal line through the center of the
        line.
        """
        return self._get_bool_prop('strike')

    @strike.setter
    def strike(self, value):
        self._set_bool_prop('strike', value)

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
        return self._get_bool_prop('webHidden')

    @web_hidden.setter
    def web_hidden(self, value):
        self._set_bool_prop('webHidden', value)

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


class _Text(object):
    """
    Proxy object wrapping ``<w:t>`` element.
    """
    def __init__(self, t_elm):
        super(_Text, self).__init__()
        self._t = t_elm
