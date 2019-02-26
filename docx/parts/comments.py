from __future__ import absolute_import, division, print_function, unicode_literals

import os

from docx.opc.constants import CONTENT_TYPE as CT
from ..opc.packuri import PackURI

from docx.oxml import parse_xml
from ..opc.part import XmlPart

class CommentsPart(XmlPart):
    """Definition of Comments Part"""

    @classmethod
    def default(cls, package):
        partname = PackURI("/word/comments.xml")
        content_type = CT.WML_COMMENTS
        element = parse_xml(cls._default_comments_xml())
        return cls(partname, content_type, element, package)
    
    @classmethod
    def _default_comments_xml(cls):
        path = os.path.join(os.path.split(__file__)[0], '..', 'templates', 'default-comments.xml')
        with open(path, 'rb') as f:
           xml_bytes = f.read()
        return xml_bytes 
