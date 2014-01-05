# encoding: utf-8

"""
Text-related proxy types for python-docx, such as Paragraph and Run.
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.enum.text import WD_BREAK


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
    Proxy object wrapping ``<w:r>`` element.
    """
    def __init__(self, r):
        super(Run, self).__init__()
        self._r = r

    def add_break(self, break_type=WD_BREAK.LINE):
        """
        Add a break element of *break_type* to this run.
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

    @property
    def bold(self):
        """
        Read/write. The bold setting for this run, one of |True|, |False|, or
        |None|. When |True|, the run will appear in bold unconditionally.
        When |False| it will appear without bold unconditionally. When
        |None|, the run will inherit its bold setting from its style
        hierarchy.
        """
        rPr = self._r.rPr
        if rPr is None:
            return None
        b = rPr.b
        if b is None:
            return None
        return b.val

    @bold.setter
    def bold(self, value):
        rPr = self._r.get_or_add_rPr()
        rPr.remove_b()
        if value is not None:
            b = rPr.add_b()
            if bool(value) is False:
                b.val = False

    @property
    def italic(self):
        """
        Read/write. The italic setting for this run, one of |True|, |False|,
        or |None|. When |True|, the run will appear in italic
        unconditionally. When |False| it will appear without italic
        unconditionally. When |None|, the run will inherit its italic setting
        from its style hierarchy.
        """
        rPr = self._r.rPr
        if rPr is None:
            return None
        i = rPr.i
        if i is None:
            return None
        return i.val

    @italic.setter
    def italic(self, value):
        rPr = self._r.get_or_add_rPr()
        rPr.remove_i()
        if value is not None:
            i = rPr.add_i()
            if bool(value) is False:
                i.val = False

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


class Text(object):
    """
    Proxy object wrapping ``<w:t>`` element.
    """
    def __init__(self, t_elm):
        super(Text, self).__init__()
        self._t = t_elm
