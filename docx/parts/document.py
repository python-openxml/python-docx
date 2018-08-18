# encoding: utf-8

"""
|DocumentPart| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..document import Document
from .numbering import NumberingPart
from ..opc.constants import RELATIONSHIP_TYPE as RT
from ..opc.part import XmlPart
from ..oxml.shape import CT_Inline
from ..shape import InlineShapes
from ..shared import lazyproperty
from .settings import SettingsPart
from .styles import StylesPart


class DocumentPart(XmlPart):
    """
    Main document part of a WordprocessingML (WML) package, aka a .docx file.
    Acts as broker to other parts such as image, core properties, and style
    parts. It also acts as a convenient delegate when a mid-document object
    needs a service involving a remote ancestor. The `Parented.part` property
    inherited by many content objects provides access to this part object for
    that purpose.
    """
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

    def get_or_add_image(self, image_descriptor):
        """
        Return an (rId, image) 2-tuple for the image identified by
        *image_descriptor*. *image* is an |Image| instance providing access
        to the properties of the image, such as dimensions and image type.
        *rId* is the key for the relationship between this document part and
        the image part, reused if already present, newly created if not.
        """
        image_part = self._package.image_parts.get_or_add_image_part(
            image_descriptor
        )
        rId = self.relate_to(image_part, RT.IMAGE)
        return rId, image_part.image

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
        id_str_lst = self._element.xpath('//@id')
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
