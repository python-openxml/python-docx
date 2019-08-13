# encoding: utf-8

"""
Run-related proxy objects for python-docx, Run in particular.
"""

from __future__ import absolute_import, print_function, unicode_literals

from ..enum.style import WD_STYLE_TYPE
from ..enum.text import WD_BREAK
from .font import Font
from ..shape import InlineShape
from ..shared import Parented


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
        inline = self.part.new_pic_inline(image_path_or_stream, width, height)
        self._r.add_drawing(inline)
        return InlineShape(inline)

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


class _Text(object):
    """
    Proxy object wrapping ``<w:t>`` element.
    """
    def __init__(self, t_elm):
        super(_Text, self).__init__()
        self._t = t_elm
