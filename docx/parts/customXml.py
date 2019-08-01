# encoding: utf-8

"""customXml part objects"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os

from ..opc.constants import CONTENT_TYPE as CT
from ..opc.packuri import PackURI
from ..opc.part import XmlPart
from ..oxml import parse_xml

class CommentsPart(XmlPart):
    """
    Comments part of a WordprocessingML (WML) package.
    """
    @classmethod
    def default(cls, package):
        """
        Return newly created empty comments part, containing only the root
        ``<w:comments>`` element.
        """
        partname = PackURI('/word/comments.xml')
        content_type = CT.WML_COMMENTS
        element = parse_xml(cls._default_comments_xml())
        return cls(partname, content_type, element, package)

    @property
    def comments(self):
        """
        A |comments| proxy object for the `w:comments` element in this part,
        containing the comments for this document.
        """
        return Comments(self.element)

    @classmethod
    def _default_comments_xml(cls):
        """
        Return a bytestream containing XML for a default settings part.
        """
        path = os.path.join(
            os.path.split(__file__)[0], '..', 'templates', 'default-comments.xml'
        )
        with open(path, 'rb') as f:
            xml_bytes = f.read()
        return xml_bytes