"""|NumberingPart| and closely related objects."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.packuri import PackURI
from docx.opc.part import XmlPart
from docx.oxml.parser import parse_xml
from docx.shared import lazyproperty

if TYPE_CHECKING:
    from docx.oxml.numbering import CT_Numbering
    from docx.package import Package


class NumberingPart(XmlPart):
    """Proxy for the numbering.xml part containing numbering definitions for a document
    or glossary."""

    @classmethod
    def new(cls, package: Package) -> "NumberingPart":
        """Return a newly created numbering part, containing only the root ``<w:numbering>``
        element."""
        partname = PackURI("/word/numbering.xml")
        content_type = CT.WML_NUMBERING
        element = cast("CT_Numbering", parse_xml(cls._default_numbering_xml()))
        return cls(partname, content_type, element, package)

    @classmethod
    def _default_numbering_xml(cls) -> bytes:
        """Return a bytestream containing XML for a default numbering part."""
        path = os.path.join(os.path.split(__file__)[0], "..", "templates", "default-numbering.xml")
        with open(path, "rb") as f:
            xml_bytes = f.read()
        return xml_bytes

    @lazyproperty
    def numbering_definitions(self):
        """The |_NumberingDefinitions| instance containing the numbering definitions
        (<w:num> element proxies) for this numbering part."""
        return _NumberingDefinitions(self._element)


class _NumberingDefinitions:
    """Collection of |_NumberingDefinition| instances corresponding to the ``<w:num>``
    elements in a numbering part."""

    def __init__(self, numbering_elm):
        super(_NumberingDefinitions, self).__init__()
        self._numbering = numbering_elm

    def __len__(self):
        return len(self._numbering.num_lst)
