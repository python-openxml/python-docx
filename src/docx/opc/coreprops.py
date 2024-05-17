"""Provides CoreProperties, Dublin-Core attributes of the document.

These are broadly-standardized attributes like author, last-modified, etc.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from docx.oxml.coreprops import CT_CoreProperties

if TYPE_CHECKING:
    from docx.oxml.coreprops import CT_CoreProperties


class CoreProperties:
    """Corresponds to part named ``/docProps/core.xml``, containing the core document
    properties for this document package."""

    def __init__(self, element: CT_CoreProperties):
        self._element = element

    @property
    def author(self):
        return self._element.author_text

    @author.setter
    def author(self, value: str):
        self._element.author_text = value

    @property
    def category(self):
        return self._element.category_text

    @category.setter
    def category(self, value: str):
        self._element.category_text = value

    @property
    def comments(self):
        return self._element.comments_text

    @comments.setter
    def comments(self, value: str):
        self._element.comments_text = value

    @property
    def content_status(self):
        return self._element.contentStatus_text

    @content_status.setter
    def content_status(self, value: str):
        self._element.contentStatus_text = value

    @property
    def created(self):
        return self._element.created_datetime

    @created.setter
    def created(self, value):
        self._element.created_datetime = value

    @property
    def identifier(self):
        return self._element.identifier_text

    @identifier.setter
    def identifier(self, value: str):
        self._element.identifier_text = value

    @property
    def keywords(self):
        return self._element.keywords_text

    @keywords.setter
    def keywords(self, value: str):
        self._element.keywords_text = value

    @property
    def language(self):
        return self._element.language_text

    @language.setter
    def language(self, value: str):
        self._element.language_text = value

    @property
    def last_modified_by(self):
        return self._element.lastModifiedBy_text

    @last_modified_by.setter
    def last_modified_by(self, value: str):
        self._element.lastModifiedBy_text = value

    @property
    def last_printed(self):
        return self._element.lastPrinted_datetime

    @last_printed.setter
    def last_printed(self, value):
        self._element.lastPrinted_datetime = value

    @property
    def modified(self):
        return self._element.modified_datetime

    @modified.setter
    def modified(self, value):
        self._element.modified_datetime = value

    @property
    def revision(self):
        return self._element.revision_number

    @revision.setter
    def revision(self, value):
        self._element.revision_number = value

    @property
    def subject(self):
        return self._element.subject_text

    @subject.setter
    def subject(self, value: str):
        self._element.subject_text = value

    @property
    def title(self):
        return self._element.title_text

    @title.setter
    def title(self, value: str):
        self._element.title_text = value

    @property
    def version(self):
        return self._element.version_text

    @version.setter
    def version(self, value: str):
        self._element.version_text = value
