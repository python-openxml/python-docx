# encoding: utf-8

"""
Document parts such as _Document, and closely related classes.
"""

from docx.enum.shape import WD_INLINE_SHAPE
from docx.opc.oxml import serialize_part_xml
from docx.opc.package import Part
from docx.oxml.shared import nsmap, oxml_fromstring
from docx.shared import lazyproperty, Parented
from docx.table import Table
from docx.text import Paragraph


class _Document(Part):
    """
    Main document part of a WordprocessingML (WML) package, aka a .docx file.
    """
    def __init__(self, partname, content_type, document_elm, package):
        super(_Document, self).__init__(
            partname, content_type, package=package
        )
        self._element = document_elm

    def add_image(self, image_descriptor):
        """
        Return an ``(image_part, rId)`` 2-tuple for the image identified by
        *image_descriptor*. *image_part* is an |Image| instance corresponding
        to the image, newly created if not already present in document. *rId*
        is the key for the relationship between this document part and the
        image part, reused if already present, newly created if not.
        """
        raise NotImplementedError

    @property
    def blob(self):
        return serialize_part_xml(self._element)

    @property
    def body(self):
        """
        The |_Body| instance containing the content for this document.
        """
        return _Body(self._element.body)

    @lazyproperty
    def inline_shapes(self):
        """
        The |InlineShapes| instance containing the inline shapes in the
        document.
        """
        return InlineShapes(self._element.body, self)

    @staticmethod
    def load(partname, content_type, blob, package):
        document_elm = oxml_fromstring(blob)
        document = _Document(partname, content_type, document_elm, package)
        return document

    @property
    def next_id(self):
        """
        The next available positive integer id value in this document. Gaps
        in id sequence are filled. The id attribute value is unique in the
        document, without regard to the element type it appears on.
        """
        raise NotImplementedError

    @property
    def part(self):
        """
        Part of the parent protocol, "children" of the document will not know
        the part that contains them so must ask their parent object. That
        chain of delegation ends here for document child objects.
        """
        return self


class _Body(object):
    """
    Proxy for ``<w:body>`` element in this document, having primarily a
    container role.
    """
    def __init__(self, body_elm):
        super(_Body, self).__init__()
        self._body = body_elm

    def add_paragraph(self):
        """
        Return a paragraph newly added to the end of body content.
        """
        p = self._body.add_p()
        return Paragraph(p)

    def add_table(self, rows, cols):
        """
        Return a table having *rows* rows and *cols* cols, newly appended to
        the main document story.
        """
        tbl = self._body.add_tbl()
        table = Table(tbl)
        for i in range(cols):
            table.columns.add()
        for i in range(rows):
            table.rows.add()
        return table

    def clear_content(self):
        """
        Return this |_Body| instance after clearing it of all content.
        Section properties for the main document story, if present, are
        preserved.
        """
        self._body.clear_content()
        return self

    @property
    def paragraphs(self):
        return [Paragraph(p) for p in self._body.p_lst]

    @property
    def tables(self):
        """
        A sequence containing all the tables in the document, in the order
        they appear.
        """
        return [Table(tbl) for tbl in self._body.tbl_lst]


class InlineShape(object):
    """
    Proxy for an ``<wp:inline>`` element, representing the container for an
    inline graphical object.
    """
    def __init__(self, inline):
        super(InlineShape, self).__init__()
        self._inline = inline

    @classmethod
    def new_picture(cls, r, image, rId, shape_id):
        """
        Return a new |InlineShape| instance containing an inline picture
        placement of the image part *image* appended to run *r* and
        uniquely identified by *shape_id*.
        """
        # width, height, filename = (
        #     image.width, image.height, image.filename
        # )
        # pic = CT_Picture.new(filename, rId, width, height)
        # inline = CT_Inline.new_inline(width, height, shape_id, pic)
        # r.add_drawing(inline)
        # return cls(inline)
        raise NotImplementedError

    @property
    def type(self):
        graphicData = self._inline.graphic.graphicData
        uri = graphicData.uri
        if uri == nsmap['pic']:
            blip = graphicData.pic.blipFill.blip
            if blip.link is not None:
                return WD_INLINE_SHAPE.LINKED_PICTURE
            return WD_INLINE_SHAPE.PICTURE
        if uri == nsmap['c']:
            return WD_INLINE_SHAPE.CHART
        if uri == nsmap['dgm']:
            return WD_INLINE_SHAPE.SMART_ART
        return WD_INLINE_SHAPE.NOT_IMPLEMENTED


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

    def add_picture(self, image_descriptor):
        """
        Add the image identified by *image_descriptor* to the document at its
        native size. The picture is placed inline in a new paragraph at the
        end of the document. *image_descriptor* can be a path (a string) or a
        file-like object containing a binary image.
        """
        rId, image = self.part.add_image(image_descriptor)
        shape_id = self.part.next_id
        r = self._body.add_p().add_r()
        return InlineShape.new_picture(r, image, rId, shape_id)

    @property
    def _inline_lst(self):
        body = self._body
        xpath = './w:p/w:r/w:drawing/wp:inline'
        return body.xpath(xpath, namespaces=nsmap)
