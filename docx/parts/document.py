# encoding: utf-8

"""
|DocumentPart| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..blkcntnr import BlockItemContainer
from ..document import Document
from .numbering import NumberingPart
from ..opc.constants import RELATIONSHIP_TYPE as RT
from ..opc.part import XmlPart
from ..shape import InlineShape
from ..shared import lazyproperty, Parented
from .styles import StylesPart


class DocumentPart(XmlPart):
    """
    Main document part of a WordprocessingML (WML) package, aka a .docx file.
    """
    @lazyproperty
    def body(self):
        """
        The |_Body| instance containing the content for this document.
        """
        return _Body(self._element.body, self)

    @property
    def core_properties(self):
        """
        A |CoreProperties| object providing read/write access to the core
        properties of this document.
        """
        return self.package.core_properties

    @property
    def document(self):
        """
        A |Document| object providing access to the content of this document.
        """
        return Document(self._element, self)

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

    def get_style(self, style_id, style_type):
        """
        Return the style in this document matching *style_id*. Returns the
        default style for *style_type* if *style_id* is |None| or does not
        match a defined style of *style_type*.
        """
        return self.styles.get_by_id(style_id, style_type)

    def get_style_id(self, style_or_name, style_type):
        """
        Return the style_id (|str|) of the style of *style_type* matching
        *style_or_name*. Returns |None| if the style resolves to the default
        style for *style_type* or if *style_or_name* is itself |None|. Raises
        if *style_or_name* is a style of the wrong type or names a style not
        present in the document.
        """
        return self.styles.get_style_id(style_or_name, style_type)

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

    @lazyproperty
    def numbering_part(self):
        """
        A |NumberingPart| object providing access to the numbering
        definitions for this document. Creates an empty numbering part if one
        is not present.
        """
        try:
            return self.part_related_by(RT.NUMBERING)
        except KeyError:
            numbering_part = NumberingPart.new()
            self.relate_to(numbering_part, RT.NUMBERING)
            return numbering_part

    def save(self, path_or_stream):
        """
        Save this document to *path_or_stream*, which can be either a path to
        a filesystem location (a string) or a file-like object.
        """
        self.package.save(path_or_stream)

    @property
    def styles(self):
        """
        A |Styles| object providing access to the styles in the styles part
        of this document.
        """
        return self._styles_part.styles

    @property
    def tables(self):
        """
        A list of |Table| instances corresponding to the tables in the
        document, in document order. Note that tables within revision marks
        such as ``<w:ins>`` or ``<w:del>`` do not appear in this list.
        """
        return self.body.tables

    @property
    def _styles_part(self):
        """
        Instance of |StylesPart| for this document. Creates an empty styles
        part if one is not present.
        """
        try:
            return self.part_related_by(RT.STYLES)
        except KeyError:
            styles_part = StylesPart.default(self.package)
            self.relate_to(styles_part, RT.STYLES)
            return styles_part


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
