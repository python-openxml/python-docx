"""|NumberingPart| and closely related objects."""

from ..opc.part import XmlPart
from ..shared import lazyproperty
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


class NumberingPart(XmlPart):
    """Proxy for the numbering.xml part containing numbering definitions for a document
    or glossary."""

    @classmethod
    def new(cls):
        """Return newly created empty numbering part, containing only the root
        ``<w:numbering>`` element."""
        xml_str = '<w:numbering {}></w:numbering>'.format(nsdecls('w'))
        numbering_xml = parse_xml(xml_str)
        content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml'
        partname = '/word/numbering.xml'

        return cls(partname, content_type, numbering_xml, None)

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
