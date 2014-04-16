# encoding: utf-8

"""
Text-related proxy types for python-docx, such as Paragraph and Run.
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.enum.text import WD_BREAK, WD_UNDERLINE


def boolproperty(f):
    """
    @boolproperty decorator. Decorated method must return the XML element
    name of the boolean property element occuring under rPr. Causes
    a read/write tri-state property to be added to the class having the name
    of the decorated function.
    """
    def _get_prop_value(parent, attr_name):
        return getattr(parent, attr_name)

    def _remove_prop(parent, attr_name):
        remove_method_name = 'remove_%s' % attr_name
        remove_method = getattr(parent, remove_method_name)
        remove_method()

    def _add_prop(parent, attr_name):
        add_method_name = 'add_%s' % attr_name
        add_method = getattr(parent, add_method_name)
        return add_method()

    def getter(obj):
        r, attr_name = obj._r, f(obj)
        if r.rPr is None:
            return None
        prop_value = _get_prop_value(r.rPr, attr_name)
        if prop_value is None:
            return None
        return prop_value.val

    def setter(obj, value):
        r, attr_name = obj._r, f(obj)
        rPr = r.get_or_add_rPr()
        _remove_prop(rPr, attr_name)
        if value is not None:
            elm = _add_prop(rPr, attr_name)
            if bool(value) is False:
                elm.val = False

    return property(getter, setter, doc=f.__doc__)


class Paragraph(object):
    """
    Proxy object wrapping ``<w:p>`` element.
    """
    def __init__(self, p):
        super(Paragraph, self).__init__()
        self._p = p

    def add_run(self, text=None):
        """
        Append a run to this paragraph.
        """
        r = self._p.add_r()
        run = Run(r)
        if text:
            run.add_text(text)
        return run

    @property
    def runs(self):
        """
        Sequence of |Run| instances corresponding to the <w:r> elements in
        this paragraph.
        """
        return [Run(r) for r in self._p.r_lst]

    @property
    def style(self):
        """
        Paragraph style for this paragraph. Read/Write.
        """
        style = self._p.style
        return style if style is not None else 'Normal'

    @style.setter
    def style(self, style):
        self._p.style = None if style == 'Normal' else style
        
    @property
    def jc(self):
        """
        Justification for this paragraph. Read/Write.
        """
        jc = self._p.jc
        return jc if jc is not None else 'start'

    @jc.setter
    def jc(self, jc):
        self._p.jc = jc

    @property
    def text(self):
        """
        A string formed by concatenating the text of each run in the
        paragraph.
        """
        text = ''
        for run in self.runs:
            text += run.text
        return text


class Run(object):
    """
    Proxy object wrapping ``<w:r>`` element. Several of the properties on Run
    take a tri-state value, |True|, |False|, or |None|. |True| and |False|
    correspond to on and off respectively. |None| indicates the property is
    not specified directly on the run and its effective value is taken from
    the style hierarchy.
    """
    def __init__(self, r):
        super(Run, self).__init__()
        self._r = r

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

    def add_text(self, text):
        """
        Add a text element to this run.
        """
        t = self._r.add_t(text)
        return Text(t)

    @boolproperty
    def all_caps(self):
        """
        Read/write. Causes the text of the run to appear in capital letters.
        """
        return 'caps'

    @boolproperty
    def bold(self):
        """
        Read/write. Causes the text of the run to appear in bold.
        """
        return 'b'

    @boolproperty
    def complex_script(self):
        """
        Read/write tri-state value. When |True|, causes the characters in the
        run to be treated as complex script regardless of their Unicode
        values.
        """
        return 'cs'

    @boolproperty
    def cs_bold(self):
        """
        Read/write tri-state value. When |True|, causes the complex script
        characters in the run to be displayed in bold typeface.
        """
        return 'bCs'

    @boolproperty
    def cs_italic(self):
        """
        Read/write tri-state value. When |True|, causes the complex script
        characters in the run to be displayed in italic typeface.
        """
        return 'iCs'

    @boolproperty
    def double_strike(self):
        """
        Read/write tri-state value. When |True|, causes the text in the run
        to appear with double strikethrough.
        """
        return 'dstrike'

    @boolproperty
    def emboss(self):
        """
        Read/write tri-state value. When |True|, causes the text in the run
        to appear as if raised off the page in relief.
        """
        return 'emboss'

    @boolproperty
    def hidden(self):
        """
        Read/write tri-state value. When |True|, causes the text in the run
        to be hidden from display, unless applications settings force hidden
        text to be shown.
        """
        return 'vanish'

    @boolproperty
    def italic(self):
        """
        Read/write tri-state value. When |True|, causes the text of the run
        to appear in italics.
        """
        return 'i'
        
    @property
    def underline(self):
        """
        Underline text with style of *underline_type*. *underline_type* can
        take the values `WD_UNDERLINE.SINGLE`, `WD_UNDERLINE.DOUBLE`, etc.
        where `WD_UNDERLINE` is imported from `docx.enum.text`.
        
        Shorthand:
        setting to True results in `WD_UNDERLINE.SINGLE`.
        setting to False results in `WD_UNDERLINE.NONE`.
        setting to None results in `WD_UNDERLINE.NONE`.
        """
        u = self._r.get_or_add_rPr().underline
        if u is None:
            return None
        return u.val

    @underline.setter
    def underline(self, utype):
        # interperate style
        if utype is None:
            utype = WD_UNDERLINE.NONE
        if type(utype)==bool:
            utype = WD_UNDERLINE.SINGLE if utype else WD_UNDERLINE.NONE
        
        u = self._r.get_or_add_rPr().underline
        if u is None:
            self._r.get_or_add_rPr().add_underline(utype)
        else:
            u.val = utype

    @boolproperty
    def imprint(self):
        """
        Read/write tri-state value. When |True|, causes the text in the run
        to appear as if pressed into the page.
        """
        return 'imprint'

    @boolproperty
    def math(self):
        """
        Read/write tri-state value. When |True|, specifies this run contains
        WML that should be handled as though it was Office Open XML Math.
        """
        return 'oMath'

    @boolproperty
    def no_proof(self):
        """
        Read/write tri-state value. When |True|, specifies that the contents
        of this run should not report any errors when the document is scanned
        for spelling and grammar.
        """
        return 'noProof'

    @boolproperty
    def outline(self):
        """
        Read/write tri-state value. When |True| causes the characters in the
        run to appear as if they have an outline, by drawing a one pixel wide
        border around the inside and outside borders of each character glyph.
        """
        return 'outline'

    @boolproperty
    def rtl(self):
        """
        Read/write tri-state value. When |True| causes the text in the run
        to have right-to-left characteristics.
        """
        return 'rtl'

    @boolproperty
    def shadow(self):
        """
        Read/write tri-state value. When |True| causes the text in the run
        to appear as if each character has a shadow.
        """
        return 'shadow'

    @boolproperty
    def small_caps(self):
        """
        Read/write tri-state value. When |True| causes the lowercase
        characters in the run to appear as capital letters two points smaller
        than the font size specified for the run.
        """
        return 'smallCaps'

    @boolproperty
    def snap_to_grid(self):
        """
        Read/write tri-state value. When |True| causes the run to use the
        document grid characters per line settings defined in the docGrid
        element when laying out the characters in this run.
        """
        return 'snapToGrid'

    @boolproperty
    def spec_vanish(self):
        """
        Read/write tri-state value. When |True|, specifies that the given run
        shall always behave as if it is hidden, even when hidden text is
        being displayed in the current document. The property has a very
        narrow, specialized use related to the table of contents. Consult the
        spec (§17.3.2.36) for more details.
        """
        return 'specVanish'

    @boolproperty
    def strike(self):
        """
        Read/write tri-state value. When |True| causes the text in the run
        to appear with a single horizontal line through the center of the
        line.
        """
        return 'strike'

    @property
    def text(self):
        """
        A string formed by concatenating all the <w:t> elements present in
        this run.
        """
        text = ''
        for t in self._r.t_lst:
            text += t.text
        return text

    @boolproperty
    def web_hidden(self):
        """
        Read/write tri-state value. When |True|, specifies that the contents
        of this run shall be hidden when the document is displayed in web
        page view.
        """
        return 'webHidden'


class Text(object):
    """
    Proxy object wrapping ``<w:t>`` element.
    """
    def __init__(self, t_elm):
        super(Text, self).__init__()
        self._t = t_elm
