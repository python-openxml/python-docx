# encoding: utf-8

"""
Custom element classes that correspond to the comments part, e.g.
<w:comments>.
"""

from .simpletypes import ST_String, ST_DecimalNumber, ST_DateTime
from .xmlchemy import (
    BaseOxmlElement, OxmlElement,
    ZeroOrOne, ZeroOrMore,
    RequiredAttribute, OptionalAttribute
)


class CT_Comment(BaseOxmlElement):
    """
    A ``<w:comment>`` element, representing a comment definition
    """

    id_comment = RequiredAttribute('w:id', ST_DecimalNumber)
    author = OptionalAttribute('w:author', ST_String)
    date = OptionalAttribute('w:date', ST_DateTime)
    initials = OptionalAttribute('w:initials', ST_String)

    def add_p(self):
        """
        Adds a new ''<w:p>'' element into this element.
        :return: a new ''<w:p>'' element.
        """
        new_paragraph = OxmlElement('w:p')
        self.append(new_paragraph)

        return new_paragraph

class CT_Comments(BaseOxmlElement):
    """
    ``<w:comments>`` element, the root element of a comments.xml file.
    """

    comment = ZeroOrMore('w:comment')

    @property
    def comment_lst(self):
        """
        Return a list containing a reference to each ``<w:comment>`` element
        in the comments, in the order encountered.
        """

        return self.xpath('.//w:comment')

    @staticmethod
    def add_comment_for(element, id_comment):
        """
        Adds comment for a element.
        :param element: An element needing a comment.
        :return: the id of this comment added.
        """

        """
        Adds a ''<w:commentRangeStart>''  as a preceding sibling directly before this element.
        """
        new_commentRgSt = OxmlElement('w:commentRangeStart')
        new_commentRgSt.id_crs = id_comment
        element.addprevious(new_commentRgSt)

        """
        Adds a ''<w:commentRangeEnd>'' element as a following sibling directly after this element.
        """
        new_commentRgEd = OxmlElement('w:commentRangeEnd')
        new_commentRgEd.id_cre = id_comment
        element.addnext(new_commentRgEd)

        """
        Adds a ''<w:commentReference>'' for this element. It is added as a following sibling directly
        after new_commentRgEd.
        """
        comment_reference = new_commentRgEd.add_commentRef()
        comment_reference.id_ref = id_comment

        return id_comment

    @staticmethod
    def get_comment_of(element):
        start = element.getprevious()
        end = element.getnext()
        ref = end.getnext()
        if isinstance(start, CT_CommentRgSt) and isinstance(end, CT_CommentRgEd) and isinstance(ref, CT_CommentRef):
            if start.id_crs == end.id_cre == ref.id_ref:
                return start, end, ref
        return None


class CT_CommentRgSt(BaseOxmlElement):
    """
    A ``<w: commentRangeStart>`` element, representing a comment definition
    """

    id_crs = RequiredAttribute('w:id', ST_DecimalNumber)
    # displacedByCustomXml = OptionalAttribute('w:displacedByCustomXml', None)


class CT_CommentRgEd(BaseOxmlElement):
    """
    A ``<w:commentRangeEnd>`` element, representing a comment definition
    """

    id_cre = RequiredAttribute('w:id', ST_DecimalNumber)
    # displacedByCustomXml = OptionalAttribute('w:displacedByCustomXml', )

    def add_commentRef(self):
        """
        Adds a ''<w:commentRef>'' element as a following sibling directly after this element.

        :return: a new ''<w:commentRef>'' element.
        """
        new_commentRef = OxmlElement('w:commentReference')
        self.addnext(new_commentRef)
        return new_commentRef


class CT_CommentRef(BaseOxmlElement):
    """
    A ``<w:comment>`` element, representing a comment definition
    """
    id_ref = RequiredAttribute('w:id', ST_DecimalNumber)
