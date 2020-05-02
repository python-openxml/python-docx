# encoding: utf-8

"""
Custom element classes related to text runs (CT_R).
"""

from ..ns import qn
from ..simpletypes import ST_BrClear, ST_BrType, ST_DecimalNumber, ST_String

from .. import OxmlElement
from ..xmlchemy import (
    BaseOxmlElement, OptionalAttribute, ZeroOrMore, ZeroOrOne ,RequiredAttribute
)

from .. import OxmlElement


class CT_Br(BaseOxmlElement):
    """
    ``<w:br>`` element, indicating a line, page, or column break in a run.
    """
    type = OptionalAttribute('w:type', ST_BrType)
    clear = OptionalAttribute('w:clear', ST_BrClear)


class CT_R(BaseOxmlElement):
    """
    ``<w:r>`` element, containing the properties and text for a run.
    """
    rPr = ZeroOrOne('w:rPr')
    ###wrong 
    ref = ZeroOrOne('w:commentRangeStart', successors=('w:r',))
    t = ZeroOrMore('w:t')
    br = ZeroOrMore('w:br')
    cr = ZeroOrMore('w:cr')
    tab = ZeroOrMore('w:tab')
    drawing = ZeroOrMore('w:drawing')

    def _insert_rPr(self, rPr):
        self.insert(0, rPr)
        return rPr

    def add_t(self, text):
        """
        Return a newly added ``<w:t>`` element containing *text*.
        """
        t = self._add_t(text=text)
        if len(text.strip()) < len(text):
            t.set(qn('xml:space'), 'preserve')
        return t

    def add_drawing(self, inline_or_anchor):
        """
        Return a newly appended ``CT_Drawing`` (``<w:drawing>``) child
        element having *inline_or_anchor* as its child.
        """
        drawing = self._add_drawing()
        drawing.append(inline_or_anchor)
        return drawing

    def add_comm(self, author, comment_part, initials, dtime, comment_text):
        
        comment = comment_part.add_comment(author, initials, dtime)
        comment._add_p(comment_text)
        # _r = self.add_r()
        self.add_comment_reference(comment._id)
        self.link_comment(comment._id)

        return comment
    
    def link_comment(self, _id):
        rStart = OxmlElement('w:commentRangeStart')
        rStart._id = _id
        rEnd = OxmlElement('w:commentRangeEnd')
        rEnd._id = _id
        self.insert(0,rStart)
        self.append(rEnd)

    def add_comment_reference(self, _id):
        reference = OxmlElement('w:commentReference')
        reference._id = _id
        self.append(reference)
        return reference
    
    def add_footnote_reference(self, _id):
        rPr = self.get_or_add_rPr()
        rstyle = rPr.get_or_add_rStyle()
        rstyle.val = 'FootnoteReference'
        reference = OxmlElement('w:footnoteReference')
        reference._id = _id
        self.append(reference)
        return reference
    
    def add_footnoteRef(self):
        ref = OxmlElement('w:footnoteRef')
        self.append(ref)

        return ref
    
    def footnote_style(self):
        rPr = self.get_or_add_rPr()
        rstyle = rPr.get_or_add_rStyle()
        rstyle.val = 'FootnoteReference'

        self.add_footnoteRef()
        return self
    
    @property
    def footnote_id(self):
        _id = self.xpath('./w:footnoteReference/@w:id')
        if len(_id) > 1 or len(_id) == 0 :
            return None
        else:
            return int(_id[0]) 

    def clear_content(self):
        """
        Remove all child elements except the ``<w:rPr>`` element if present.
        """
        content_child_elms = self[1:] if self.rPr is not None else self[:]
        for child in content_child_elms:
            self.remove(child)

    def add_comment_reference(self, _id):
        reference = OxmlElement('w:commentReference')
        reference._id = _id
        self.append(reference)
        return reference

    @property
    def style(self):
        """
        String contained in w:val attribute of <w:rStyle> grandchild, or
        |None| if that element is not present.
        """
        rPr = self.rPr
        if rPr is None:
            return None
        return rPr.style

    @style.setter
    def style(self, style):
        """
        Set the character style of this <w:r> element to *style*. If *style*
        is None, remove the style element.
        """
        rPr = self.get_or_add_rPr()
        rPr.style = style

    @property
    def text(self):
        """
        A string representing the textual content of this run, with content
        child elements like ``<w:tab/>`` translated to their Python
        equivalent.
        """
        text = ''
        for child in self:
            if child.tag == qn('w:t'):
                t_text = child.text
                text += t_text if t_text is not None else ''
            elif child.tag == qn('w:tab'):
                text += '\t'
            elif child.tag in (qn('w:br'), qn('w:cr')):
                text += '\n'
            elif child.tag == qn('w:noBreakHyphen'):
                text += '-'
        return text

    @text.setter
    def text(self, text):
        self.clear_content()
        _RunContentAppender.append_to_run_from_text(self, text)


class CT_Text(BaseOxmlElement):
    """
    ``<w:t>`` element, containing a sequence of characters within a run.
    """


class CT_RPr(BaseOxmlElement):
    rStyle  = ZeroOrOne('w:rStyle')
     

class CT_RStyle(BaseOxmlElement):
    val = RequiredAttribute('w:val',ST_String)

class _RunContentAppender(object):
    """
    Service object that knows how to translate a Python string into run
    content elements appended to a specified ``<w:r>`` element. Contiguous
    sequences of regular characters are appended in a single ``<w:t>``
    element. Each tab character ('\t') causes a ``<w:tab/>`` element to be
    appended. Likewise a newline or carriage return character ('\n', '\r')
    causes a ``<w:cr>`` element to be appended.
    """
    def __init__(self, r):
        self._r = r
        self._bfr = []

    @classmethod
    def append_to_run_from_text(cls, r, text):
        """
        Create a "one-shot" ``_RunContentAppender`` instance and use it to
        append the run content elements corresponding to *text* to the
        ``<w:r>`` element *r*.
        """
        appender = cls(r)
        appender.add_text(text)

    def add_text(self, text):
        """
        Append the run content elements corresponding to *text* to the
        ``<w:r>`` element of this instance.
        """
        for char in text:
            self.add_char(char)
        self.flush()

    def add_char(self, char):
        """
        Process the next character of input through the translation finite
        state maching (FSM). There are two possible states, buffer pending
        and not pending, but those are hidden behind the ``.flush()`` method
        which must be called at the end of text to ensure any pending
        ``<w:t>`` element is written.
        """
        if char == '\t':
            self.flush()
            self._r.add_tab()
        elif char in '\r\n':
            self.flush()
            self._r.add_br()
        else:
            self._bfr.append(char)

    def flush(self):
        text = ''.join(self._bfr)
        if text:
            self._r.add_t(text)
        del self._bfr[:]


