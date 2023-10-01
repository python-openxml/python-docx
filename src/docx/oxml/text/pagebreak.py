"""Custom element class for rendered page-break (CT_LastRenderedPageBreak)."""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from docx.oxml.xmlchemy import BaseOxmlElement
from docx.shared import lazyproperty

if TYPE_CHECKING:
    from docx.oxml.text.hyperlink import CT_Hyperlink
    from docx.oxml.text.paragraph import CT_P


class CT_LastRenderedPageBreak(BaseOxmlElement):
    """`<w:lastRenderedPageBreak>` element, indicating page break inserted by renderer.

    A rendered page-break is one inserted by the renderer when it runs out of room on a
    page. It is an empty element (no attrs or children) and is a child of CT_R, peer to
    CT_Text.

    NOTE: this complex-type name does not exist in the schema, where
    `w:lastRenderedPageBreak` maps to `CT_Empty`. This name was added to give it
    distinguished behavior. CT_Empty is used for many elements.
    """

    @property
    def precedes_all_content(self) -> bool:
        """True when a `w:lastRenderedPageBreak` precedes all paragraph content.

        This is a common case; it occurs whenever the page breaks on an even paragraph
        boundary.
        """
        # -- a page-break inside a hyperlink never meets these criteria because there
        # -- is always part of the hyperlink text before the page-break.
        if self._is_in_hyperlink:
            return False

        return bool(
            # -- XPath will match zero-or-one w:lastRenderedPageBreak element --
            self._enclosing_p.xpath(
                # -- in first run of paragraph --
                f"./w:r[1]"
                # -- all page-breaks --
                f"/w:lastRenderedPageBreak"
                # -- that are not preceded by any content-bearing elements --
                f"[not(preceding-sibling::*[{self._run_inner_content_xpath}])]"
            )
        )

    @property
    def preceding_fragment_p(self) -> CT_P:
        """A "loose" `CT_P` containing only the paragraph content before this break.

        Raises `ValueError` if this `w:lastRenderedPageBreak` is not the first rendered
        paragraph in its paragraph.

        The returned `CT_P` is a "clone" (deepcopy) of the `w:p` ancestor of this
        page-break with this `w:lastRenderedPageBreak` element and all its following
        siblings removed.
        """
        if not self == self._first_lrpb_in_p(self._enclosing_p):
            raise ValueError("only defined on first rendered page-break in paragraph")

        # -- splitting approach is different when break is inside a hyperlink --
        return (
            self._preceding_frag_in_hlink
            if self._is_in_hyperlink
            else self._preceding_frag_in_run
        )

    def _enclosing_hyperlink(self, lrpb: CT_LastRenderedPageBreak) -> CT_Hyperlink:
        """The `w:hyperlink` grandparent of this `w:lastRenderedPageBreak`.

        Raises `IndexError` when this page-break has a `w:p` grandparent, so only call
        when `._is_in_hyperlink` is True.
        """
        return lrpb.xpath("./parent::w:r/parent::w:hyperlink")[0]

    @property
    def _enclosing_p(self) -> CT_P:
        """The `w:p` element parent or grandparent of this `w:lastRenderedPageBreak`."""
        return self.xpath("./ancestor::w:p[1]")[0]

    def _first_lrpb_in_p(self, p: CT_P) -> CT_LastRenderedPageBreak:
        """The first `w:lastRenderedPageBreak` element in `p`.

        Raises `ValueError` if there are no rendered page-breaks in `p`.
        """
        lrpbs = p.xpath(
            "./w:r/w:lastRenderedPageBreak | ./w:hyperlink/w:r/w:lastRenderedPageBreak"
        )
        if not lrpbs:
            raise ValueError("no rendered page-breaks in paragraph element")
        return lrpbs[0]

    @lazyproperty
    def _is_in_hyperlink(self) -> bool:
        """True when this page-break is embedded in a hyperlink run."""
        return bool(self.xpath("./parent::w:r/parent::w:hyperlink"))

    @lazyproperty
    def _preceding_frag_in_hlink(self) -> CT_P:
        """Preceding CT_P fragment when break occurs within a hyperlink.

        Note this is a *partial-function* and raises when `lrpb` is not inside a
        hyperlink.
        """
        if not self._is_in_hyperlink:
            raise ValueError("only defined on a rendered page-break in a hyperlink")

        # -- work on a clone `w:p` so our mutations don't persist --
        p = copy.deepcopy(self._enclosing_p)

        # -- get this `w:lastRenderedPageBreak` in the cloned `w:p` (not self) --
        lrpb = self._first_lrpb_in_p(p)

        # -- locate `w:hyperlink` in which this `w:lastRenderedPageBreak` is found --
        hyperlink = lrpb._enclosing_hyperlink(lrpb)

        # -- delete all w:p inner-content following the hyperlink --
        for e in hyperlink.xpath("./following-sibling::*"):
            p.remove(e)

        # -- remove this page-break from inside the hyperlink --
        lrpb.getparent().remove(lrpb)

        # -- that's it, the entire hyperlink goes into the preceding fragment so
        # -- the hyperlink is not "split".
        return p

    @lazyproperty
    def _preceding_frag_in_run(self) -> CT_P:
        """Preceding CT_P fragment when break does not occur in a hyperlink.

        Note this is a *partial-function* and raises when `lrpb` is inside a hyperlink.
        """
        if self._is_in_hyperlink:
            raise ValueError("only defined on a rendered page-break not in a hyperlink")

        # -- work on a clone `w:p` so our mutations don't persist --
        p = copy.deepcopy(self._enclosing_p)

        # -- get this `w:lastRenderedPageBreak` in the cloned `w:p` (not self) --
        lrpb = self._first_lrpb_in_p(p)

        # -- locate `w:r` in which this `w:lastRenderedPageBreak` is found --
        enclosing_r = lrpb.xpath("./parent::w:r")[0]

        # -- delete all `w:p` inner-content following that run --
        for e in enclosing_r.xpath("./following-sibling::*"):
            p.remove(e)

        # -- then delete all `w:r` inner-content following this lrpb in its run and
        # -- also remove the page-break itself
        for e in lrpb.xpath("./following-sibling::*"):
            enclosing_r.remove(e)
        enclosing_r.remove(lrpb)

        return p

    @lazyproperty
    def _run_inner_content_xpath(self) -> str:
        """XPath fragment matching any run inner-content elements."""
        return (
            "self::w:br"
            " | self::w:cr"
            " | self::w:drawing"
            " | self::w:noBreakHyphen"
            " | self::w:ptab"
            " | self::w:t"
            " | self::w:tab"
        )
