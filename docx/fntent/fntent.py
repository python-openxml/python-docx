# encoding: utf-8


from __future__ import absolute_import, division, print_function, unicode_literals

from docx.shared import ElementProxy
from ..text.paragraph import Paragraph
from ..shared import Parented

class Footnotes(ElementProxy):
    """
    Footnotes object, container for all objects in the footnotes part

    Accessed using the :attr:`.Document.footnotes` property. Supports ``len()``, iteration,
    and dictionary-style access by footnote id.
    """

    def __init__(self, element, part):
        super(Footnotes, self).__init__(element)
        self._part = part

    @property
    def part(self):
        """
        The |FootnotesPart| object of this document.
        """
        return self._part


    @property
    def footnotes(self):
        return [Footnote(footnote, self) for footnote in self._element.footnote_lst]

    def get_by_id(self, footnote_id):
        """Return the footnote matching *footnote_id*.

        Returns |None| if not found.
        """
        return self._get_by_id(footnote_id)

    def _get_by_id(self, footnote_id):
        """
        Return the footnote matching *footnote_id*.
        """
        footnote = self._element.get_by_id(footnote_id)

        if footnote is None:
            return None

        return Footnote(footnote, self)


class Footnote(Parented):
    """
    Proxy object wrapping ``<w:footnote>`` element.
    """

    def __init__(self, footnote, parent):
        super(Footnote, self).__init__(parent)
        self._element = footnote


    @property
    def paragraphs(self):
        """
        Returns a list of paragraph proxy object
        """

        return [Paragraph(p, self) for p in self._element.p_lst]


class Endnotes(ElementProxy):
    """
    Endnotes object, container for all objects in the endnotes part

    Accessed using the :attr:`.Document.endnotes` property. Supports ``len()``, iteration,
    and dictionary-style access by endnote id.
    """

    def __init__(self, element, part):
        super(Endnotes, self).__init__(element)
        self._part = part

    @property
    def part(self):
        """
        The |EndnotesPart| object of this document.
        """
        return self._part

    @property
    def endnotes(self):
        return [Endnote(endnote, self) for endnote in self._element.endnote_lst]

    def get_by_id(self, endnote_id):
        """Return the endnote matching *endnote_id*.

        Returns |None| if not found.
        """
        return self._get_by_id(endnote_id)

    def _get_by_id(self, endnote_id):
        """
        Return the endnote matching *endnote_id*.
        """
        endnote = self._element.get_by_id(endnote_id)

        if endnote is None:
            return None

        return Endnote(endnote, self)


class Endnote(Parented):
    """
    Proxy object wrapping ``<w:endnote>`` element.
    """

    def __init__(self, endnote, parent):
        super(Endnote, self).__init__(parent)
        self._element = endnote

    @property
    def paragraphs(self):
        """
        Returns a list of paragraph proxy object
        """

        return [Paragraph(p, self) for p in self._element.p_lst]
