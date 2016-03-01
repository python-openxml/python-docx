from ..oxml.shape import CT_Inline
from ..opc.constants import RELATIONSHIP_TYPE as RT
from ..opc.part import XmlPart
from ..shape import InlineShapes
from ..shared import lazyproperty
from .styles import StylesPart


class HeaderPart(XmlPart):
    @property
    def _styles_part(self):
        """
        Instance of |StylesPart| for this document. Creates an empty styles
        part if one is not present.
        """
        # HACK
        # one styles to rule them all, maybe this is the way it's supposed to be?
        document = self.package.main_document_part
        try:
            return document.part_related_by(RT.STYLES)
        except KeyError:
            styles_part = StylesPart.default(self.package)
            document.relate_to(styles_part, RT.STYLES)
            return styles_part

    # MOSTLY COPYPASTA FROM DOCUMENT PART BELOW THIS POINT
    # TODO ABSTRACT?
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
    def styles(self):
        """
        A |Styles| object providing access to the styles in the styles part
        of this document.
        """
        return self._styles_part.styles


class FooterPart(HeaderPart):
    # identical to HeaderPart, ABSTRACT
    pass
