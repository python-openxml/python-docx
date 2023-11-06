"""Settings object, providing access to document-level settings."""

from docx.shared import ElementProxy


class Settings(ElementProxy):
    """Provides access to document-level settings for a document.

    Accessed using the :attr:`.Document.settings` property.
    """

    @property
    def odd_and_even_pages_header_footer(self):
        """True if this document has distinct odd and even page headers and footers.

        Read/write.
        """
        return self._element.evenAndOddHeaders_val

    @property
    def track_revisions(self):
        """
		True if this document has track revisions feature enabled.

        Read/write.
        """
        return self._element.trackRevisions_val

    @odd_and_even_pages_header_footer.setter
    def odd_and_even_pages_header_footer(self, value):
        self._element.evenAndOddHeaders_val = value

    @track_revisions.setter
    def track_revisions(self, value):
        self._element.trackRevisions_val = value
