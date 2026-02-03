# pyright: reportImportCycles=false

"""Block item container, used by body, cell, header, etc.

Block level items are things like paragraph and table, although there are a few other
specialized ones like structured document tags.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from typing_extensions import TypeAlias

from docx.oxml.ns import qn
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.shared import StoryChild
from docx.text.paragraph import Paragraph

if TYPE_CHECKING:
    import docx.types as t
    from docx.oxml.comments import CT_Comment
    from docx.oxml.document import CT_Body
    from docx.oxml.section import CT_HdrFtr
    from docx.oxml.table import CT_Tc
    from docx.revision import TrackedDeletion, TrackedInsertion
    from docx.shared import Length
    from docx.styles.style import ParagraphStyle
    from docx.table import Table

BlockItemElement: TypeAlias = "CT_Body | CT_Comment | CT_HdrFtr | CT_Tc"


class BlockItemContainer(StoryChild):
    """Base class for proxy objects that can contain block items.

    These containers include _Body, _Cell, header, footer, footnote, endnote, comment,
    and text box objects. Provides the shared functionality to add a block item like a
    paragraph or table.
    """

    def __init__(self, element: BlockItemElement, parent: t.ProvidesStoryPart):
        super(BlockItemContainer, self).__init__(parent)
        self._element = element

    def add_paragraph(self, text: str = "", style: str | ParagraphStyle | None = None) -> Paragraph:
        """Return paragraph newly added to the end of the content in this container.

        The paragraph has `text` in a single run if present, and is given paragraph
        style `style`.

        If `style` is |None|, no paragraph style is applied, which has the same effect
        as applying the 'Normal' style.
        """
        paragraph = self._add_paragraph()
        if text:
            paragraph.add_run(text)
        if style is not None:
            paragraph.style = style
        return paragraph

    def add_table(self, rows: int, cols: int, width: Length) -> Table:
        """Return table of `width` having `rows` rows and `cols` columns.

        The table is appended appended at the end of the content in this container.

        `width` is evenly distributed between the table columns.
        """
        from docx.table import Table

        tbl = CT_Tbl.new_tbl(rows, cols, width)
        self._element._insert_tbl(tbl)  # pyright: ignore[reportPrivateUsage]
        return Table(tbl, self)

    def iter_inner_content(
        self, include_revisions: bool = False
    ) -> Iterator[Paragraph | Table | TrackedInsertion | TrackedDeletion]:
        """Generate each `Paragraph` or `Table` in this container in document order.

        Args:
            include_revisions: If True, also yields `TrackedInsertion` and
                `TrackedDeletion` objects for block-level tracked changes
                (`w:ins` and `w:del` elements that wrap paragraphs or tables).
                Defaults to False for backward compatibility.

        Yields:
            Paragraph, Table, TrackedInsertion, or TrackedDeletion objects in
            document order.
        """
        from docx.revision import TrackedDeletion, TrackedInsertion
        from docx.table import Table

        if include_revisions:
            elements = getattr(self._element, "inner_content_with_revisions", None)
            if elements is None:
                elements = self._element.inner_content_elements
        else:
            elements = self._element.inner_content_elements

        for element in elements:
            tag = element.tag  # pyright: ignore[reportUnknownMemberType]
            if tag == qn("w:p"):
                yield Paragraph(element, self)
            elif tag == qn("w:tbl"):
                yield Table(element, self)
            elif tag == qn("w:ins"):
                yield TrackedInsertion(element, self)  # pyright: ignore[reportArgumentType]
            elif tag == qn("w:del"):
                yield TrackedDeletion(element, self)  # pyright: ignore[reportArgumentType]

    @property
    def paragraphs(self):
        """A list containing the paragraphs in this container, in document order.

        Read-only.
        """
        return [Paragraph(p, self) for p in self._element.p_lst]

    @property
    def tables(self):
        """A list containing the tables in this container, in document order.

        Read-only.
        """
        from docx.table import Table

        return [Table(tbl, self) for tbl in self._element.tbl_lst]

    def _add_paragraph(self):
        """Return paragraph newly added to the end of the content in this container."""
        return Paragraph(self._element.add_p(), self)
