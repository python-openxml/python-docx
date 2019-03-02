# encoding: utf-8

"""The |Altchunk| and closely objects"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx import Document
from ..opc.part import Part
from io import BytesIO

class AltchunkPart(Part):
    """AltChunkPart for word document

    An AltChunk is a nested word document
    """
    def __init__(self, partname, content_type, element, package):
        super(AltchunkPart, self).__init__(
            partname, content_type, package=package
        )
        self._element = element

    @property
    def blob(self):
        stream = BytesIO()
        self._element.save(stream)
        return stream.getvalue()

    @property
    def element(self):
        """
        The root XML element of this XML part.
        """
        return self._element

    @classmethod
    def load(cls, partname, content_type, blob, package):
        # TODO: is this a good place to catch the XMLSyntaxError and try
        # parsing as a ZipFile? Perhaps this should be overridden int he
        # document_part class definition since is seems to be specific to
        # document chunks???

        element = Document(BytesIO(blob)) 
        # alternatively docx.api.Package.open(BytesIO(blob))
        # Aside: element.part.package.main_document_part is element.part -> True
        return cls(partname, content_type, element, package)

    @property
    def part(self):
        """
        Part of the parent protocol, "children" of the document will not know
        the part that contains them so must ask their parent object. That
        chain of delegation ends here for child objects.
        """
        return self


