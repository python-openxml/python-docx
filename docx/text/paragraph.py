# encoding: utf-8

"""
Paragraph-related proxy types.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..enum.style import WD_STYLE_TYPE
from .parfmt import ParagraphFormat
from .run import Run
from ..shared import Parented

from datetime import datetime
import re

class Paragraph(Parented):
    """
    Proxy object wrapping ``<w:p>`` element.
    """
    def __init__(self, p, parent):
        super(Paragraph, self).__init__(parent)
        self._p = self._element = p

    def add_run(self, text=None, style=None):
        """
        Append a run to this paragraph containing *text* and having character
        style identified by style ID *style*. *text* can contain tab
        (``\\t``) characters, which are converted to the appropriate XML form
        for a tab. *text* can also include newline (``\\n``) or carriage
        return (``\\r``) characters, each of which is converted to a line
        break.
        """
        r = self._p.add_r()
        run = Run(r, self)
        if text:
            run.text = text
        if style:
            run.style = style
        return run
    
    def delete(self):
        """
        delete the content of the paragraph
        """
        self._p.getparent().remove(self._p)
        self._p = self._element = None
    
    def add_comment(self, text, author='python-docx', initials='pd', dtime=None ,rangeStart=0, rangeEnd=0):
        comment_part = self.part._comments_part.element
        if dtime is None:
            dtime = str( datetime.now() ).replace(' ', 'T')
        comment =  self._p.add_comm(author, comment_part, initials, dtime, text, rangeStart, rangeEnd)

        return comment
    
    def add_footnote(self, text):
        footnotes_part = self.part._footnotes_part.element
        footnote = self._p.add_fn(text, footnotes_part)

        return footnote

    def merge_paragraph(self, otherParagraph):
        r_lst = otherParagraph.runs
        self.append_runs(r_lst)
    
    def append_runs(self, runs):
        self.add_run(' ')
        for run in runs:
            self._p.append(run._r)
            
    
    @property
    def alignment(self):
        """
        A member of the :ref:`WdParagraphAlignment` enumeration specifying
        the justification setting for this paragraph. A value of |None|
        indicates the paragraph has no directly-applied alignment value and
        will inherit its alignment value from its style hierarchy. Assigning
        |None| to this property removes any directly-applied alignment value.
        """
        return self._p.alignment

    @alignment.setter
    def alignment(self, value):
        self._p.alignment = value

    def clear(self):
        """
        Return this same paragraph after removing all its content.
        Paragraph-level formatting, such as style, is preserved.
        """
        self._p.clear_content()
        return self

    def insert_paragraph_before(self, text=None, style=None):
        """
        Return a newly created paragraph, inserted directly before this
        paragraph. If *text* is supplied, the new paragraph contains that
        text in a single run. If *style* is provided, that style is assigned
        to the new paragraph.
        """
        paragraph = self._insert_paragraph_before()
        if text:
            paragraph.add_run(text)
        if style is not None:
            paragraph.style = style
        return paragraph

    @property
    def paragraph_format(self):
        """
        The |ParagraphFormat| object providing access to the formatting
        properties for this paragraph, such as line spacing and indentation.
        """
        return ParagraphFormat(self._element)

    @property
    def runs(self):
        """
        Sequence of |Run| instances corresponding to the <w:r> elements in
        this paragraph.
        """
        return [Run(r, self) for r in self._p.r_lst]

    @property
    def style(self):
        """
        Read/Write. |_ParagraphStyle| object representing the style assigned
        to this paragraph. If no explicit style is assigned to this
        paragraph, its value is the default paragraph style for the document.
        A paragraph style name can be assigned in lieu of a paragraph style
        object. Assigning |None| removes any applied style, making its
        effective value the default paragraph style for the document.
        """
        style_id = self._p.style
        return self.part.get_style(style_id, WD_STYLE_TYPE.PARAGRAPH)

    @style.setter
    def style(self, style_or_name):
        style_id = self.part.get_style_id(
            style_or_name, WD_STYLE_TYPE.PARAGRAPH
        )
        self._p.style = style_id

    @property
    def text(self):
        """
        String formed by concatenating the text of each run in the paragraph.
        Tabs and line breaks in the XML are mapped to ``\\t`` and ``\\n``
        characters respectively.

        Assigning text to this property causes all existing paragraph content
        to be replaced with a single run containing the assigned text.
        A ``\\t`` character in the text is mapped to a ``<w:tab/>`` element
        and each ``\\n`` or ``\\r`` character is mapped to a line break.
        Paragraph-level formatting, such as style, is preserved. All
        run-level formatting, such as bold or italic, is removed.
        """
        text = ''
        for run in self.runs:
            text += run.text
        return text

    @property
    def header_level(self):
        '''
        input Paragraph Object
        output Paragraph level in case of header or returns None
        '''
        headerPattern = re.compile(".*Heading (\d+)$")
        level = 0
        if headerPattern.match(self.style.name):
            level = int(self.style.name.lower().split('heading')[-1].strip())
        return level
    
    @property
    def NumId(self):
        '''
        returns NumId val in case of paragraph has numbering
        else: return None
        '''
        try:
            return self._p.pPr.numPr.numId.val
        except:
            return None
    
    @property
    def list_lvl(self):
        '''
        returns ilvl val in case of paragraph has a numbering level
        else: return None
        '''
        try:
            return self._p.pPr.numPr.ilvl.val
        except :
            return None
    
    @property
    def list_info(self):
        '''
        returns tuple (has numbering info, numId value, ilvl value)
        '''
        if self.NumId and self.list_lvl:
            return True, self.NumId, self.list_lvl
        else:
            return False, 0, 0
    
    @property
    def is_heading(self):
        return True if self.header_level else False
    
    @property
    def full_text(self):
        allRuns = [Run(r, self) for r in self._p.xpath('.//w:r[not(ancestor::w:r)]')]
        return u"".join([r.text for r in allRuns])
    
    @property
    def footnotes(self):
        if self._p.footnote_ids is not None :
            return True
        else :
            return False

    @text.setter
    def text(self, text):
        self.clear()
        self.add_run(text)

    def _insert_paragraph_before(self):
        """
        Return a newly created paragraph, inserted directly before this
        paragraph.
        """
        p = self._p.add_p_before()
        return Paragraph(p, self._parent)
