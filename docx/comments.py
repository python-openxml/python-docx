# encoding: utf-8

"""Comments object, providing access to comments"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.shared import ElementProxy
from docx.text.paragraph import Paragraph
from docx.blkcntnr import BlockItemContainer


class Comments(ElementProxy):

    def __init__(self, element):
        super(Comments, self).__init__(element)

    def add_comment(self):
        """
        Adds a new comment for the comments.
        :return: a new comment.
        """
        id_ = self.next_id
        comment = Comment(self._element.add_comment(),self)
        comment.id_comment = id_
        return comment

    def get_comment_by_id(self, id_comment):
        """
        Finds a comment by a id.
        :param id_comment: a id of comment.
        :return: a comment instance in this comments.
        """
        for comment in self._comment_lst():
            if comment.id_comment == id_comment:
                return comment

    def _comment_lst(self):
        for comment in self._element.comment_lst:
            yield Comment(comment, self)

    @property
    def comment_lst(self):
        """
        Finds all comment.
        :return: A list of |Comment| instances.
        """
        return [comment for comment in self._comment_lst()]

    @property
    def next_id(self):
        """
        Finds all maximum id of comments to add one as next id to void repeat.
        :return: a new id.
        """
        comment_list = self.comment_lst
        if len(comment_list)>0:
            id_list = [comment.id_comment for comment in comment_list]
            return max(id_list) + 1
        else:
            return 0

    def add_comment_for(self, block, text=''):
        """
        Adds comment for block having _element. The content of the comment is the text.
        :param block: a element needing a comment.
        :param text:  the content of the comment.
        :return: comment.
        """
        comment = self.add_comment()
        paragraph = comment.add_paragraph(text)
        self._element.add_comment_for(block._element, comment.id_comment)

        return comment

    def get_comment_of(self, block):
        """
        Gets comment of a block if it exist, or return None
        :param block: a paragraph, a run, a table, or a table cell, etc.
        :return ( commentRangeStart, commentRangeEnd, commentReference ) or None
        """
        return self._element.get_comment_of(block._element)

    def remove_comment(self, comment):
        """
        Remove a element.
        :param comment: a comment needed to remove.
        """
        self._element.remove(comment._element)


class Comment(BlockItemContainer):

    def __init__(self, element, parent):
        super(Comment, self).__init__(element, parent)
        self._element = element

    @property
    def id_comment(self):

        return self._element.id_comment

    @id_comment.setter
    def id_comment(self, id_comment):
        """
        Sets a id for this comment, the type of the id is int.
        :param id_comment: a new id.
        """
        self._element.id_comment = id_comment

    @property
    def author(self):
        """
        Gets the author of this comment.
        :return: a string.
        """
        return self._element.author

    @author.setter
    def author(self, author):
        """
        Sets author for this comment.
        :param author: a string.
        """
        self._element.author = author

    @property
    def date(self):
        """
        Gets a date of this comment created. It is a string.
        e.g. comment.date = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
        it is a right instance.
        :return: a date.
        """
        return self._element.date

    @date.setter
    def date(self, date):
        """
        Sets a date for this comment. It is a string.
        :param date: a string representing date.
        """
        self._element.date = date

    @property
    def element(self):
        """
        Gets a instance of CT_Comment.
        :return: a instance of CT_Comment.
        """
        return self._element
