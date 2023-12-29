"""The |Footnotes| object and related proxy classes."""

from __future__ import annotations

from docx.blkcntnr import BlockItemContainer
from docx.shared import Parented


class Footnotes(Parented):
    """
    Proxy object wrapping ``<w:footnotes>`` element.
    """
    def __init__(self, footnotes, parent):
        super(Footnotes, self).__init__(parent)
        self._element = self._footnotes = footnotes

    def __getitem__(self, reference_id):
        """
        A |Footnote| for a specific footnote of reference id, defined with ``w:id`` argument of ``<w:footnoteReference>``.
        If reference id is invalid raises an |IndexError|
        """
        footnote = self._element.get_by_id(reference_id)
        if footnote is None:
            raise IndexError
        return Footnote(footnote, self)

    def __len__(self):
        return len(self._element)

    def add_footnote(self, footnote_reference_id):
        """
        Return a newly created |Footnote|, the new footnote will
        be inserted in the correct spot by `footnote_reference_id`.
        The footnotes are kept in order by `footnote_reference_id`.
        """
        elements = self._element # for easy access
        new_footnote = None
        if elements.get_by_id(footnote_reference_id) is not None:
            # When adding a footnote it can be inserted 
            # in front of some other footnotes, so
            # we need to sort footnotes by `footnote_reference_id`
            # in |Footnotes| and in |Paragraph|
            #
            # resolve reference ids in |Footnotes|
            # iterate in reverse and compare the current
            # id with the inserted id. If there are the same
            # insert the new footnote in that place, if not
            # increment the current footnote id.
            for index in reversed(range(len(elements))):
                if elements[index].id == footnote_reference_id:
                    elements[index].id += 1
                    new_footnote = elements[index].add_footnote_before(footnote_reference_id)
                    break
                else:
                    elements[index].id += 1
        else:
            # append the newly created |Footnote| to |Footnotes|
            new_footnote = elements.add_footnote(footnote_reference_id)
        return Footnote(new_footnote, self)


class Footnote(BlockItemContainer):
    """
    Proxy object wrapping ``<w:footnote>`` element.
    """
    def __init__(self, f, parent):
        super(Footnote, self).__init__(f, parent)
        self._f = self._element = f

    def __eq__(self, other):
        if isinstance(other, Footnote):
            return self._f is other._f
        return False

    def __ne__(self, other):
        if isinstance(other, Footnote):
            return self._f is not other._f
        return True

    @property
    def id(self):
        return self._f.id
