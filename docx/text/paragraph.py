# encoding: utf-8

"""
Paragraph-related proxy types.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
import re

from ..enum.style import WD_STYLE_TYPE
from .parfmt import ParagraphFormat
from .run import Run
from ..shared import Parented


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

    def replace_text(self, old, new):
        """
        Replace all occurrences of old string in the paragraph with the new one
        :param old: old string to replace
        :param new: new string to write
        """
        positions = [(a.start(), a.end() -1) for a in re.finditer(old,self.text)]
        l_run = self.runs
        i_pos = 0
        j_run = 0
        virtual_start = 0
        if (len(positions)> 0):
            occurrences_finished = False   # loop over runs finishes when all occurrences are processed
            while (not occurrences_finished):
                r = l_run[j_run]
                virtual_stop = virtual_start + len(r.text) -1
                # now consider the 5 cases (behaviour copied from Libre Office)
                # 1. start of run is part of suffix of old : delete the part of the string for run
                # 2. old is all contained in run : replace
                # 3. start of old is suffix of run : replace
                # 4. run is a substring of old : delete the text
                pos = positions[i_pos]
                len_original_text = len(r.text)
                load_next_run = False
                while (pos[0] <= virtual_stop and not load_next_run):
                    if (pos[0] < virtual_start and pos[1] <= virtual_stop):
                        # case 1
                        tmp_old = old[-(pos[1]-virtual_start+1):]
                        tmp_text = r.text.replace(tmp_old, '')
                        r.replace_text(tmp_text)

                    if (pos[0] >= virtual_start and pos[1] <= virtual_stop):
                        # case 2
                        tmp_text = r.text.replace(old, new)
                        r.replace_text(tmp_text)

                    if (pos[0] >= virtual_start and pos[1] > virtual_stop):
                        # case 3
                        tmp_old = old[:virtual_stop - pos[0] +1]
                        tmp_text = r.text.replace(tmp_old, new)
                        r.replace_text(tmp_text)
                        load_next_run = True

                    if (pos[0] < virtual_start and pos[1] > virtual_stop):
                        # case 4
                        r.replace_text('')
                        load_next_run = True

                    if (not load_next_run):
                        i_pos += 1
                        if (i_pos < len(positions)):
                            pos = positions[i_pos]
                        else:
                            occurrences_finished = True
                            load_next_run = True
                j_run += 1
                virtual_start += len_original_text


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
