# encoding: utf-8

"""
|DocumentPart| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from collections import Sequence

from ..blkcntnr import BlockItemContainer
from ..enum.section import WD_SECTION
from ..opc.constants import RELATIONSHIP_TYPE as RT
from ..opc.package import XmlPart
from ..section import Section
from ..shape import InlineShape
from ..shared import lazyproperty, Parented


class DocumentPart(XmlPart):
    """
    Main document part of a WordprocessingML (WML) package, aka a .docx file.
    """
    def add_paragraph(self, text='', style=None):
        """
        Return a paragraph newly added to the end of body content.
        """
        return self.body.add_paragraph(text, style)

    def add_section(self, start_type=WD_SECTION.NEW_PAGE):
        """
        Return a |Section| object representing a new section added at the end
        of the document.
        """
        new_sectPr = self._element.body.add_section_break()
        new_sectPr.start_type = start_type
        return Section(new_sectPr)

    def add_table(self, rows, cols):
        """
        Return a table having *rows* rows and *cols* columns, newly appended
        to the main document story.
        """
        return self.body.add_table(rows, cols)

    @lazyproperty
    def body(self):
        """
        The |_Body| instance containing the content for this document.
        """
        return _Body(self._element.body, self)

    def get_or_add_image_part(self, image_descriptor):
        """
        Return an ``(image_part, rId)`` 2-tuple for the image identified by
        *image_descriptor*. *image_part* is an |Image| instance corresponding
        to the image, newly created if no matching image part is found. *rId*
        is the key for the relationship between this document part and the
        image part, reused if already present, newly created if not.
        """
        image_parts = self._package.image_parts
        image_part = image_parts.get_or_add_image_part(image_descriptor)
        rId = self.relate_to(image_part, RT.IMAGE)
        return (image_part, rId)

    @lazyproperty
    def inline_shapes(self):
        """
        The |InlineShapes| instance containing the inline shapes in the
        document.
        """
        return InlineShapes(self._element.body, self)

    @property
    def next_id(self):
        """
        The next available positive integer id value in this document. Gaps
        in id sequence are filled. The id attribute value is unique in the
        document, without regard to the element type it appears on.
        """
        id_str_lst = self._element.xpath('//@id')
        used_ids = [int(id_str) for id_str in id_str_lst if id_str.isdigit()]
        for n in range(1, len(used_ids)+2):
            if n not in used_ids:
                return n

    @property
    def paragraphs(self):
        """
        A list of |Paragraph| instances corresponding to the paragraphs in
        the document, in document order. Note that paragraphs within revision
        marks such as inserted or deleted do not appear in this list.
        """
        return self.body.paragraphs

    @lazyproperty
    def sections(self):
        """
        The |Sections| instance organizing the sections in this document.
        """
        return Sections(self._element)

    @property
    def tables(self):
        """
        A list of |Table| instances corresponding to the tables in the
        document, in document order. Note that tables within revision marks
        such as ``<w:ins>`` or ``<w:del>`` do not appear in this list.
        """
        return self.body.tables


class _Body(BlockItemContainer):
    """
    Proxy for ``<w:body>`` element in this document, having primarily a
    container role.
    """
    def __init__(self, body_elm, parent):
        super(_Body, self).__init__(body_elm, parent)
        self._body = body_elm

    def clear_content(self):
        """
        Return this |_Body| instance after clearing it of all content.
        Section properties for the main document story, if present, are
        preserved.
        """
        self._body.clear_content()
        return self


class InlineShapes(Parented):
    """
    Sequence of |InlineShape| instances, supporting len(), iteration, and
    indexed access.
    """
    def __init__(self, body_elm, parent):
        super(InlineShapes, self).__init__(parent)
        self._body = body_elm

    def __getitem__(self, idx):
        """
        Provide indexed access, e.g. 'inline_shapes[idx]'
        """
        try:
            inline = self._inline_lst[idx]
        except IndexError:
            msg = "inline shape index [%d] out of range" % idx
            raise IndexError(msg)
        return InlineShape(inline)

    def __iter__(self):
        return (InlineShape(inline) for inline in self._inline_lst)

    def __len__(self):
        return len(self._inline_lst)

    def add_picture(self, image_descriptor, run):
        """
        Return an |InlineShape| instance containing the picture identified by
        *image_descriptor* and added to the end of *run*. The picture shape
        has the native size of the image. *image_descriptor* can be a path (a
        string) or a file-like object containing a binary image.
        """
        image_part, rId = self.part.get_or_add_image_part(image_descriptor)
        shape_id = self.part.next_id
        r = run._r
        picture = InlineShape.new_picture(r, image_part, rId, shape_id)
        return picture

    @property
    def _inline_lst(self):
        body = self._body
        xpath = '//w:p/w:r/w:drawing/wp:inline'
        return body.xpath(xpath)


class Sections(Sequence):
    """
    Sequence of |Section| objects corresponding to the sections in the
    document. Supports ``len()``, iteration, and indexed access.
    """
    def __init__(self, document_elm):
        super(Sections, self).__init__()
        self._document_elm = document_elm

    def __getitem__(self, key):
        if isinstance(key, slice):
            sectPr_lst = self._document_elm.sectPr_lst[key]
            return [Section(sectPr) for sectPr in sectPr_lst]
        sectPr = self._document_elm.sectPr_lst[key]
        return Section(sectPr)

    def __iter__(self):
        for sectPr in self._document_elm.sectPr_lst:
            yield Section(sectPr)

    def __len__(self):
        return len(self._document_elm.sectPr_lst)
