# encoding: utf-8

"""|DocumentPart| and closely related objects"""

from __future__ import absolute_import, division, print_function, unicode_literals

from itertools import chain

from docx.bookmark import Bookmarks
from docx.document import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.shape import CT_Inline
from docx.parts.hdrftr import FooterPart, HeaderPart
from docx.parts.numbering import NumberingPart
from docx.parts.settings import SettingsPart
from docx.parts.story import BaseStoryPart
from docx.parts.styles import StylesPart
from docx.shape import InlineShapes
from docx.shared import lazyproperty


class DocumentPart(BaseStoryPart):
    """Main document part of a WordprocessingML (WML) package, aka a .docx file.

    Acts as broker to other parts such as image, core properties, and style parts. It
    also acts as a convenient delegate when a mid-document object needs a service
    involving a remote ancestor. The `Parented.part` property inherited by many content
    objects provides access to this part object for that purpose.
    """

    def add_footer_part(self):
        """Return (footer_part, rId) pair for newly-created footer part."""
        footer_part = FooterPart.new(self.package)
        rId = self.relate_to(footer_part, RT.FOOTER)
        return footer_part, rId

    def add_header_part(self):
        """Return (header_part, rId) pair for newly-created header part."""
        header_part = HeaderPart.new(self.package)
        rId = self.relate_to(header_part, RT.HEADER)
        return header_part, rId

    @lazyproperty
    def bookmarks(self):
        """Singleton |Bookmarks| object for this docx package."""
        return Bookmarks(self)

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

    def drop_header_part(self, rId):
        """Remove related header part identified by *rId*."""
        self.drop_rel(rId)

    def footer_part(self, rId):
        """Return |FooterPart| related by *rId*."""
        return self.related_parts[rId]

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

    def header_part(self, rId):
        """Return |HeaderPart| related by *rId*."""
        return self.related_parts[rId]

    @lazyproperty
    def inline_shapes(self):
        """
        The |InlineShapes| instance containing the inline shapes in the
        document.
        """
        return InlineShapes(self._element.body, self)

    def iter_story_parts(self):
        """Generate all parts in document that contain a story.

        A story is a sequence of block-level items (paragraphs and tables).
        Story parts include this main document part, headers, footers,
        footnotes, and endnotes.
        """
        return chain(
            (self,),
            self.iter_parts_related_by(
                {RT.COMMENTS, RT.ENDNOTES, RT.FOOTER, RT.FOOTNOTES, RT.HEADER}
            ),
        )

    def new_pic_inline(self, image_descriptor, width, height):
        """
        Return a newly-created `w:inline` element containing the image
        specified by *image_descriptor* and scaled based on the values of
        *width* and *height*.
        """
        rId, image = self.get_or_add_image(image_descriptor)
        cx, cy = image.scaled_dimensions(width, height)
        shape_id, filename = self.next_id, image.filename
        return CT_Inline.new_pic_inline(shape_id, rId, filename, cx, cy)

    @property
    def next_id(self):
        """Next available positive integer id value in this document.

        Calculated by incrementing maximum existing id value. Gaps in the
        existing id sequence are not filled. The id attribute value is unique
        in the document, without regard to the element type it appears on.
        """
        id_str_lst = self._element.xpath("//@id")
        used_ids = [int(id_str) for id_str in id_str_lst if id_str.isdigit()]
        if not used_ids:
            return 1
        return max(used_ids) + 1

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

    def related_hdrftr_body(self, rId):
        """
        Return the |HeaderFooterBody| object corresponding to the related
        part identified by *rId*.
        """
        raise NotImplementedError

    def save(self, path_or_stream):
        """
        Save this document to *path_or_stream*, which can be either a path to
        a filesystem location (a string) or a file-like object.
        """
        self.package.save(path_or_stream)

    @property
    def settings(self):
        """
        A |Settings| object providing access to the settings in the settings
        part of this document.
        """
        return self._settings_part.settings

    @property
    def styles(self):
        """
        A |Styles| object providing access to the styles in the styles part
        of this document.
        """
        return self._styles_part.styles

    @property
    def _settings_part(self):
        """
        A |SettingsPart| object providing access to the document-level
        settings for this document. Creates a default settings part if one is
        not present.
        """
        try:
            return self.part_related_by(RT.SETTINGS)
        except KeyError:
            settings_part = SettingsPart.default(self.package)
            self.relate_to(settings_part, RT.SETTINGS)
            return settings_part

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
