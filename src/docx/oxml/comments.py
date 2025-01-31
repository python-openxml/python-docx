import random
from typing import TYPE_CHECKING, Callable, List, Optional, cast

from docx.oxml.parser import OxmlElement
from docx.oxml.simpletypes import ST_DecimalNumber, ST_String, XsdBoolean
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OneOrMore,
    OptionalAttribute,
    RequiredAttribute,
    ZeroOrOne,
)

if TYPE_CHECKING:
    from docx.oxml.text.paragraph import CT_P


class CT_Comment(BaseOxmlElement):
    """``<w:comment>`` element."""

    add_paragraph: Callable[[], "CT_P"]

    id = RequiredAttribute("w:id", ST_DecimalNumber)
    author = RequiredAttribute("w:author", ST_String)
    initials = RequiredAttribute("w:initials", ST_String)
    date = RequiredAttribute("w:date", ST_String)
    paragraph = ZeroOrOne("w:p", successors=("w:comment",))

    def add_para(self, para):
        """Add a paragraph to the comment."""
        para_id = self.get_random_id()
        para.para_id = para_id
        self._insert_paragraph(para)

    @property
    def para_id(self) -> ST_String:
        """Return the paragraph id of the comment"""
        return self.paragraph.para_id

    @para_id.setter
    def para_id(self, value: ST_String):
        self.paragraph.para_id = value

    @staticmethod
    def get_random_id() -> ST_String:
        """Generates a random id"""
        return cast(ST_String, hex(random.getrandbits(24))[2:].upper())


class CT_Comments(BaseOxmlElement):
    """``<w:comments>`` element, the root element of the comments part."""

    add_comments: Callable[[], CT_Comment]
    comments = OneOrMore("w:comment")

    @property
    def _next_comment_id(self) -> int:
        """Return the next comment ID to use."""
        comment_ids: List[int] = [
            int(id_str) for id_str in self.xpath("./w:comment/@w:id") if id_str.isdigit()
        ]
        return max(comment_ids) + 1 if len(comment_ids) > 0 else 1

    def add_comment(self, para: "CT_P", author: str, initials: str, date: str) -> "CT_Comment":
        """Return comment added to this part."""
        comment_id = self._next_comment_id
        comment = self.add_comments()
        comment.id = comment_id
        comment.author = author
        comment.initials = initials
        comment.date = date
        comment.add_para(para)
        return comment


class CT_CommentRangeStart(BaseOxmlElement):

    _id = RequiredAttribute("w:id", ST_DecimalNumber)

    @classmethod
    def new(cls, _id: ST_DecimalNumber) -> "CT_CommentRangeStart":
        """Return a new ``<w:commentRangeStart>`` element having id `id`."""
        comment_range_start = OxmlElement("w:commentRangeStart")
        comment_range_start._id = _id
        return comment_range_start


class CT_CommentRangeEnd(BaseOxmlElement):

    _id = RequiredAttribute("w:id", ST_DecimalNumber)

    @classmethod
    def new(cls, _id: ST_DecimalNumber) -> "CT_CommentRangeEnd":
        """Return a new ``<w:commentRangeEnd>`` element having id `id`."""
        comment_range_end = OxmlElement("w:commentRangeEnd")
        comment_range_end._id = _id
        return comment_range_end


class CT_CommentReference(BaseOxmlElement):

    _id = RequiredAttribute("w:id", ST_DecimalNumber)

    @classmethod
    def new(cls, _id: ST_DecimalNumber) -> "CT_CommentReference":
        """Return a new ``<w:commentReference>`` element having id `id`."""
        comment_reference = OxmlElement("w:commentReference")
        comment_reference._id = _id
        return comment_reference


class CT_CommentExtended(BaseOxmlElement):
    """``<w15:commentEx>`` element, the root element of the commentsExtended part."""

    para_id = RequiredAttribute("w15:paraId", ST_String)
    resolved = RequiredAttribute("w15:done", XsdBoolean)
    parent_para_id = OptionalAttribute("w15:paraIdParent", ST_String)


class CT_CommentsExtended(BaseOxmlElement):
    """``<w15:commentsEx>`` element, the root element of the commentsExtended part."""

    add_comments_extended_sequence: Callable[[], CT_CommentExtended]
    comments_extended_sequence = OneOrMore("w15:commentEx")

    def add_comment_reference(
        self,
        comment: str,
        parent: Optional[str] = None,
        resolved: Optional[bool] = False,
    ) -> CT_CommentExtended:
        """Add a reply to the comment identified by `parent_comment_id`."""
        comment_ext = self.add_comments_extended_sequence()
        comment_ext.para_id = comment.para_id
        if parent is not None:
            comment_ext.parent_para_id = parent.para_id
        comment_ext.resolved = resolved
        return comment_ext

    def get_element(self, para_id: str) -> Optional[CT_CommentExtended]:
        """Return the comment extended element for the given paragraph id"""
        try:
            return self.xpath(f"./w15:commentEx[@w15:paraId='{para_id}']")[0]
        except:
            raise KeyError(f"no <w15:commentEx> element with paraId {para_id}")
