"""
Run item container, used by paragraph, hyperlink.
"""

from __future__ import absolute_import, print_function

from .shared import Parented
from .text.run import Run


class RunItemContainer(Parented):
    def __init__(self, element, parent):
        super(RunItemContainer, self).__init__(parent)
        self._element = element

    def add_run(self, text=None, style=None):
        """
        Append a run to this container containing *text* and having character
        style identified by style ID *style*. *text* can contain tab
        (``\\t``) characters, which are converted to the appropriate XML form
        for a tab. *text* can also include newline (``\\n``) or carriage
        return (``\\r``) characters, each of which is converted to a line
        break.
        """
        r = self._element.add_r()
        run = Run(r, self)
        if text:
            run.text = text
        if style:
            run.style = style
        return run

    @property
    def runs(self):
        """
        Sequence of |Run| instances corresponding to the <w:r> elements in
        this container.
        """
        return [Run(r, self) for r in self._element.r_lst]

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
