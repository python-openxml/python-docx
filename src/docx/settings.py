"""Settings object, providing access to document-level settings."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from docx.shared import ElementProxy

if TYPE_CHECKING:
    import docx.types as t
    from docx.oxml.settings import CT_Settings
    from docx.oxml.xmlchemy import BaseOxmlElement


class Settings(ElementProxy):
    """Provides access to document-level settings for a document.

    Accessed using the :attr:`.Document.settings` property.
    """

    def __init__(self, element: BaseOxmlElement, parent: t.ProvidesXmlPart | None = None):
        super().__init__(element, parent)
        self._settings = cast("CT_Settings", element)

    @property
    def odd_and_even_pages_header_footer(self) -> bool:
        """True if this document has distinct odd and even page headers and footers.

        Read/write.
        """
        return self._settings.evenAndOddHeaders_val

    @odd_and_even_pages_header_footer.setter
    def odd_and_even_pages_header_footer(self, value: bool):
        self._settings.evenAndOddHeaders_val = value

    @property
    def track_revisions(self) -> bool:
        """True if track-changes is enabled for this document.

        Read/write. When True, changes made to the document will be tracked as
        revisions. When False, changes are applied directly without tracking.
        """
        return self._settings.trackRevisions_val

    @track_revisions.setter
    def track_revisions(self, value: bool):
        self._settings.trackRevisions_val = value
