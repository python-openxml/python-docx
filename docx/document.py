# encoding: utf-8

"""
|Document| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .oxml import OxmlElement
from .oxml.header import CT_Hdr, CT_Ftr
from .oxml.ns import qn, nsmap
from .opc.constants import RELATIONSHIP_TYPE as RT, CONTENT_TYPE as CT
from .opc.packuri import PackURI
from .parts.header import HeaderPart, FooterPart
from .header import Header, Footer
from .blkcntnr import BlockItemContainer
from .enum.section import WD_SECTION
from .enum.text import WD_BREAK
from .section import Section, Sections
from .shared import ElementProxy, Emu


class Document(ElementProxy):
    """
    WordprocessingML (WML) document. Not intended to be constructed directly.
    Use :func:`docx.Document` to open or create a document.
    """

    __slots__ = ('_part', '__body')

    def __init__(self, element, part):
        super(Document, self).__init__(element)
        self._part = part
        self.__body = None

    def add_heading(self, text='', level=1):
        """
        Return a heading paragraph newly added to the end of the document,
        containing *text* and having its paragraph style determined by
        *level*. If *level* is 0, the style is set to `Title`. If *level* is
        1 (or omitted), `Heading 1` is used. Otherwise the style is set to
        `Heading {level}`. Raises |ValueError| if *level* is outside the
        range 0-9.
        """
        if not 0 <= level <= 9:
            raise ValueError("level must be in range 0-9, got %d" % level)
        style = 'Title' if level == 0 else 'Heading %d' % level
        return self.add_paragraph(text, style)

    def add_page_break(self):
        """
        Return a paragraph newly added to the end of the document and
        containing only a page break.
        """
        paragraph = self.add_paragraph()
        paragraph.add_run().add_break(WD_BREAK.PAGE)
        return paragraph

    def add_paragraph(self, text='', style=None):
        """
        Return a paragraph newly added to the end of the document, populated
        with *text* and having paragraph style *style*. *text* can contain
        tab (``\\t``) characters, which are converted to the appropriate XML
        form for a tab. *text* can also include newline (``\\n``) or carriage
        return (``\\r``) characters, each of which is converted to a line
        break.
        """
        return self._body.add_paragraph(text, style)

    def add_picture(self, image_path_or_stream, width=None, height=None):
        """
        Return a new picture shape added in its own paragraph at the end of
        the document. The picture contains the image at
        *image_path_or_stream*, scaled based on *width* and *height*. If
        neither width nor height is specified, the picture appears at its
        native size. If only one is specified, it is used to compute
        a scaling factor that is then applied to the unspecified dimension,
        preserving the aspect ratio of the image. The native size of the
        picture is calculated using the dots-per-inch (dpi) value specified
        in the image file, defaulting to 72 dpi if no value is specified, as
        is often the case.
        """
        run = self.add_paragraph().add_run()
        return run.add_picture(image_path_or_stream, width, height)

    def add_section(self, start_type=WD_SECTION.NEW_PAGE):
        """
        Return a |Section| object representing a new section added at the end
        of the document. The optional *start_type* argument must be a member
        of the :ref:`WdSectionStart` enumeration, and defaults to
        ``WD_SECTION.NEW_PAGE`` if not provided.
        """
        new_sectPr = self._element.body.add_section_break()
        new_sectPr.start_type = start_type
        return Section(new_sectPr)

    def add_table(self, rows, cols, style=None):
        """
        Add a table having row and column counts of *rows* and *cols*
        respectively and table style of *style*. *style* may be a paragraph
        style object or a paragraph style name. If *style* is |None|, the
        table inherits the default table style of the document.
        """
        table = self._body.add_table(rows, cols, self._block_width)
        table.style = style
        return table

    @property
    def headers(self):
        raise NotImplementedError('todo')

    def add_header(self):
        """
        removes all headers from doc then adds a new one
        """
        # TODO raise exception if header present, telling user to remove them first!
        # dont clear headers invisibly
        self.remove_headers()
        return self._body.add_header()

    def add_footer(self):
        """
        removes all footers from doc then adds a new one
        """
        # TODO raise exception if footer present, telling user to remove them first!
        # dont clear footers invisibly
        self.remove_footers()
        return self._body.add_footer()

    def remove_headers(self):
        """
        clears existing header elements and references from document
        """
        self._body.remove_headers()

    def remove_footers(self):
        """
        clears existing footer elements and references from document
        """
        self._body.remove_footers()

    @property
    def core_properties(self):
        """
        A |CoreProperties| object providing read/write access to the core
        properties of this document.
        """
        return self._part.core_properties

    @property
    def inline_shapes(self):
        """
        An |InlineShapes| object providing access to the inline shapes in
        this document. An inline shape is a graphical object, such as
        a picture, contained in a run of text and behaving like a character
        glyph, being flowed like other text in a paragraph.
        """
        return self._part.inline_shapes

    @property
    def paragraphs(self):
        """
        A list of |Paragraph| instances corresponding to the paragraphs in
        the document, in document order. Note that paragraphs within revision
        marks such as ``<w:ins>`` or ``<w:del>`` do not appear in this list.
        """
        return self._body.paragraphs

    @property
    def part(self):
        """
        The |DocumentPart| object of this document.
        """
        return self._part

    def save(self, path_or_stream):
        """
        Save this document to *path_or_stream*, which can be either a path to
        a filesystem location (a string) or a file-like object.
        """
        self._part.save(path_or_stream)

    @property
    def sections(self):
        """
        A |Sections| object providing access to each section in this
        document.
        """
        return Sections(self._element)

    @property
    def settings(self):
        """
        A |Settings| object providing access to the document-level settings
        for this document.
        """
        return self._part.settings

    @property
    def styles(self):
        """
        A |Styles| object providing access to the styles in this document.
        """
        return self._part.styles

    @property
    def tables(self):
        """
        A list of |Table| instances corresponding to the tables in the
        document, in document order. Note that only tables appearing at the
        top level of the document appear in this list; a table nested inside
        a table cell does not appear. A table within revision marks such as
        ``<w:ins>`` or ``<w:del>`` will also not appear in the list.
        """
        return self._body.tables

    @property
    def _block_width(self):
        """
        Return a |Length| object specifying the width of available "writing"
        space between the margins of the last section of this document.
        """
        section = self.sections[-1]
        return Emu(
            section.page_width - section.left_margin - section.right_margin
        )

    @property
    def _body(self):
        """
        The |_Body| instance containing the content for this document.
        """
        if self.__body is None:
            self.__body = _Body(self._element.body, self)
        return self.__body


class _Body(BlockItemContainer):
    """
    Proxy for ``<w:body>`` element in this document, having primarily a
    container role.
    """
    def __init__(self, body_elm, parent):
        super(_Body, self).__init__(body_elm, parent)
        self._body = body_elm

    def add_header(self):
        rel_id = self._parent.part.rels._next_rId

        # make header_ref_elm
        header_ref_elm_tag = 'w:headerReference'
        header_attrs = {
            qn('r:id'): rel_id,
            qn('w:type'): "default"
        }
        header_ref_elm = OxmlElement(header_ref_elm_tag, attrs=header_attrs)

        # make header_elm
        header_elm = CT_Hdr.new()

        # make target part
        partname = PackURI('/word/header1.xml')
        content_type = CT.WML_HEADER
        header_part = HeaderPart(partname, content_type, header_elm, self._parent._part.package)

        # make header instance (wrapper around elm)
        header = Header(header_elm, self._parent, header_part)

        reltype = nsmap['r'] + '/header'
        self._parent.part.rels.add_relationship(reltype, header_part, rel_id)

        sentinel_sectPr = self._body.get_or_add_sectPr()
        sentinel_sectPr.insert(0, header_ref_elm)
        return header

    def add_footer(self):
        rel_id = self._parent.part.rels._next_rId

        # make footer_ref_elm
        footer_ref_elm_tag = 'w:footerReference'
        footer_attrs = {
            qn('r:id'): rel_id,
            qn('w:type'): "default"
        }
        footer_ref_elm = OxmlElement(footer_ref_elm_tag, attrs=footer_attrs)

        # make footer_elm
        footer_elm = CT_Ftr.new()

        # make target part
        partname = PackURI('/word/footer1.xml')
        content_type = CT.WML_FOOTER
        footer_part = FooterPart(partname, content_type, footer_elm, self._parent._part.package)

        # make footer instance (wrapper around elm)
        footer = Footer(footer_elm, self, footer_part)

        reltype = nsmap['r'] + '/footer'
        self._parent.part.rels.add_relationship(reltype, footer_part, rel_id)

        sentinel_sectPr = self._body.get_or_add_sectPr()
        # TODO check whether there is headerRef and decide 0 or 1
        sentinel_sectPr.insert(1, footer_ref_elm)
        return footer

    def remove_headers(self):
        """
        clears existing header elements and references from sentinel sect pr
        """
        header_elm_tag = 'w:headerReference'
        sentinel_sectPr = self._body.get_or_add_sectPr()
        sentinel_sectPr.remove_all(header_elm_tag)

        header_rel_ids = [rel_id for rel_id, rel in self._parent.part.rels.items() if rel.reltype == RT.HEADER]
        for rel_id in header_rel_ids:
            self.part.rels.remove_relationship(rel_id)

    def remove_footers(self):
        """
        clears existing footer elements and references from sentinel sect pr
        """
        footer_elm_tag = 'w:footerReference'
        sentinel_sectPr = self._body.get_or_add_sectPr()
        sentinel_sectPr.remove_all(footer_elm_tag)

        footer_rel_ids = [rel_id for rel_id, rel in self._parent.part.rels.items() if rel.reltype == RT.FOOTER]
        for rel_id in footer_rel_ids:
            self.part.rels.remove_relationship(rel_id)

    def clear_content(self):
        """
        Return this |_Body| instance after clearing it of all content.
        Section properties for the main document story, if present, are
        preserved.
        """
        self._body.clear_content()
        return self
