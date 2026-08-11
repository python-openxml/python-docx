"""|NumberingPart| and closely related objects."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docx.opc.constants import CONTENT_TYPE as CT
from docx.oxml.ns import nsdecls
from docx.oxml.parser import parse_xml
from docx.opc.part import XmlPart
from docx.shared import lazyproperty

if TYPE_CHECKING:
    from docx.package import Package


class NumberingPart(XmlPart):
    """Proxy for the numbering.xml part containing numbering definitions for a document
    or glossary."""

    @classmethod
    def new(cls, package: Package) -> "NumberingPart":
        """Return newly created numbering part, containing only the root ``<w:numbering>``
        element."""
        partname = package.next_partname("/word/numbering%d.xml")
        content_type = CT.WML_NUMBERING
        element = parse_xml("<w:numbering %s/>" % nsdecls("w"))
        return cls(partname, content_type, element, package)

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
