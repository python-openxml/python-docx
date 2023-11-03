"""Hyperlink-related proxy objects for python-docx, Hyperlink in particular.

A hyperlink occurs in a paragraph, at the same level as a Run, and a hyperlink itself
contains runs, which is where the visible text of the hyperlink is stored. So it's kind
of in-between, less than a paragraph and more than a run. So it gets its own module.
"""

from __future__ import annotations

from typing import List

from docx import types as t
from docx.oxml.text.hyperlink import CT_Hyperlink
from docx.shared import Parented
from docx.text.run import Run


class Hyperlink(Parented):
    """Proxy object wrapping a `<w:hyperlink>` element.

    A hyperlink occurs as a child of a paragraph, at the same level as a Run. A
    hyperlink itself contains runs, which is where the visible text of the hyperlink is
    stored.
    """

    def __init__(self, hyperlink: CT_Hyperlink, parent: t.ProvidesStoryPart):
        super().__init__(parent)
        self._parent = parent
        self._hyperlink = self._element = hyperlink

    @property
    def address(self) -> str:
        """The "URL" of the hyperlink (but not necessarily a web link).

        While commonly a web link like "https://google.com" the hyperlink address can
        take a variety of forms including "internal links" to bookmarked locations
        within the document. When this hyperlink is an internal "jump" to for example a
        heading from the table-of-contents (TOC), the address is blank. The bookmark
        reference (like "_Toc147925734") is stored in the `.fragment` property.
        """
        rId = self._hyperlink.rId
        return self._parent.part.rels[rId].target_ref if rId else ""

    @property
    def contains_page_break(self) -> bool:
        """True when the text of this hyperlink is broken across page boundaries.

        This is not uncommon and can happen for example when the hyperlink text is
        multiple words and occurs in the last line of a page. Theoretically, a hyperlink
        can contain more than one page break but that would be extremely uncommon in
        practice. Still, this value should be understood to mean that "one-or-more"
        rendered page breaks are present.
        """
        return bool(self._hyperlink.lastRenderedPageBreaks)

    @property
    def fragment(self) -> str:
        """Reference like `#glossary` at end of URL that refers to a sub-resource.

        Note that this value does not include the fragment-separator character ("#").

        This value is known as a "named anchor" in an HTML context and "anchor" in the
        MS API, but an "anchor" element (`<a>`) represents a full hyperlink in HTML so
        we avoid confusion by using the more precise RFC 3986 naming "URI fragment".

        These are also used to refer to bookmarks within the same document, in which
        case the `.address` value with be blank ("") and this property will hold a
        value like "_Toc147925734".

        To reliably get an entire web URL you will need to concatenate this with the
        `.address` value, separated by "#" when both are present. Consider using the
        `.url` property for that purpose.

        Word sometimes stores a fragment in this property (an XML attribute) and
        sometimes with the address, depending on how the URL is inserted, so don't
        depend on this field being empty to indicate no fragment is present.
        """
        return self._hyperlink.anchor or ""

    @property
    def runs(self) -> List[Run]:
        """List of |Run| instances in this hyperlink.

        Together these define the visible text of the hyperlink. The text of a hyperlink
        is typically contained in a single run will be broken into multiple runs if for
        example part of the hyperlink is bold or the text was changed after the document
        was saved.
        """
        return [Run(r, self._parent) for r in self._hyperlink.r_lst]

    @property
    def text(self) -> str:
        """String formed by concatenating the text of each run in the hyperlink.

        Tabs and line breaks in the XML are mapped to ``\\t`` and ``\\n`` characters
        respectively. Note that rendered page-breaks can occur within a hyperlink but
        they are not reflected in this text.
        """
        return self._hyperlink.text

    @property
    def url(self) -> str:
        """Convenience property to get web URLs from hyperlinks that contain them.

        This value is the empty string ("") when there is no address portion, so its
        boolean value can also be used to distinguish external URIs from internal "jump"
        hyperlinks like those found in a table-of-contents.

        Note that this value may also be a link to a file, so if you only want web-urls
        you'll need to check for a protocol prefix like `https://`.

        When both an address and fragment are present, the return value joins the two
        separated by the fragment-separator hash ("#"). Otherwise this value is the same
        as that of the `.address` property.
        """
        address, fragment = self.address, self.fragment
        if not address:
            return ""
        return f"{address}#{fragment}" if fragment else address
