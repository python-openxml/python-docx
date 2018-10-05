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

import copy
import collections


class Paragraph(Parented):
    """
    Proxy object wrapping ``<w:p>`` element.
    """
    def __init__(self, p, parent):
        super(Paragraph, self).__init__(parent)
        self._p = self._element = p

    def copy(self):
        """
        Returns a copy of this paragraph
        """
        return Paragraph(copy.deepcopy(self._element), None)

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

    def replace(self, old, new, count=None):
        """
        Searches the paragraph for all occurrences of string *old* replaced by
        *new*. If the optional argument *count* is given, only the first *count*
        occurrences are replaced. Return this same paragraph.

        Try to keep the Run structure as unaltered as possible: text is replaced
        inside the run where it has been found. If the found text spawns across
        multiple runs, the whole new text is placed in the run where the old
        text started.
        """
        # Loop counter
        replaced = 0
        # Search start index
        start = 0
        while count is None or replaced < count:
            replaced += 1

            # Phase 1: analyze the paragraph, build text with metadata.
            #
            # This will contain the full text contained in the paragraph,
            # as string (just like self.text property)
            text = ''
            # This will contain the map of the sources for every letter,
            # consisting of a list of tuples ( run_instance, index_inside_run )
            origins = []
            for run in self.runs:
                for run_idx, letter in enumerate(run.text):
                    text += letter
                    origins.append( (run, run_idx) )
            # Maybe this is paranoid, just to be sure
            assert len(text) == len(origins)

            # Phase 2: search for next occurrence of text to be replaced and,
            #          if found, build a list of the affected runs.
            match_idx = text.find(old, start)
            if match_idx == -1:
                # Nothing to replace, I'm done
                break
            # This will contain a dict of the affected runs, in the form
            # run_instance: { 'start': start_index, 'end': end_index }
            affected_runs = collections.OrderedDict()
            for idx in range(match_idx, match_idx + len(old)):
                run, run_idx = origins[idx]
                if run not in affected_runs.keys():
                    # This is the first character inside that run,
                    # create a new entry
                    affected_runs[run] = {
                        'start': run_idx,
                        'end': run_idx,
                    }
                else:
                    # Yet one more character fot this run, move the end forward
                    affected_runs[run]['end'] = run_idx
            # Yet another paranoid assert?
            assert len(affected_runs) > 0

            # Phase 3: Finally replace the text inside the first run, just clear
            # the text from subsequent runs
            first = True
            for run, rc in affected_runs.items():
                if first:
                    first = False
                    repl = new
                else:
                    repl = ''
                run.text = run.text[:rc['start']] + repl + run.text[rc['end']+1:]

            # Phase 4: move search start forward
            start = start + len(new)

        return self

    def _insert_paragraph_before(self):
        """
        Return a newly created paragraph, inserted directly before this
        paragraph.
        """
        p = self._p.add_p_before()
        return Paragraph(p, self._parent)
