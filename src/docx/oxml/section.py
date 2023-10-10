"""Section-related custom element classes."""

from __future__ import annotations

from copy import deepcopy
from typing import Callable, Iterator, Sequence, Union, cast

from lxml import etree
from typing_extensions import TypeAlias

from docx.enum.section import WD_HEADER_FOOTER, WD_ORIENTATION, WD_SECTION_START
from docx.oxml.ns import nsmap
from docx.oxml.shared import CT_OnOff
from docx.oxml.simpletypes import ST_SignedTwipsMeasure, ST_TwipsMeasure, XsdString
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OptionalAttribute,
    RequiredAttribute,
    ZeroOrMore,
    ZeroOrOne,
)
from docx.shared import Length, lazyproperty

BlockElement: TypeAlias = Union[CT_P, CT_Tbl]


class CT_HdrFtr(BaseOxmlElement):
    """`w:hdr` and `w:ftr`, the root element for header and footer part respectively."""

    p = ZeroOrMore("w:p", successors=())
    tbl = ZeroOrMore("w:tbl", successors=())


class CT_HdrFtrRef(BaseOxmlElement):
    """`w:headerReference` and `w:footerReference` elements."""

    type_: WD_HEADER_FOOTER = (
        RequiredAttribute(  # pyright: ignore[reportGeneralTypeIssues]
            "w:type", WD_HEADER_FOOTER
        )
    )
    rId: str = RequiredAttribute(  # pyright: ignore[reportGeneralTypeIssues]
        "r:id", XsdString
    )


class CT_PageMar(BaseOxmlElement):
    """``<w:pgMar>`` element, defining page margins."""

    top: Length | None = OptionalAttribute(  # pyright: ignore[reportGeneralTypeIssues]
        "w:top", ST_SignedTwipsMeasure
    )
    right: Length | None = OptionalAttribute(  # pyright: ignore
        "w:right", ST_TwipsMeasure
    )
    bottom: Length | None = OptionalAttribute(  # pyright: ignore
        "w:bottom", ST_SignedTwipsMeasure
    )
    left: Length | None = OptionalAttribute(  # pyright: ignore[reportGeneralTypeIssues]
        "w:left", ST_TwipsMeasure
    )
    header: Length | None = OptionalAttribute(  # pyright: ignore
        "w:header", ST_TwipsMeasure
    )
    footer: Length | None = OptionalAttribute(  # pyright: ignore
        "w:footer", ST_TwipsMeasure
    )
    gutter: Length | None = OptionalAttribute(  # pyright: ignore
        "w:gutter", ST_TwipsMeasure
    )


class CT_PageSz(BaseOxmlElement):
    """``<w:pgSz>`` element, defining page dimensions and orientation."""

    w: Length | None = OptionalAttribute(  # pyright: ignore[reportGeneralTypeIssues]
        "w:w", ST_TwipsMeasure
    )
    h: Length | None = OptionalAttribute(  # pyright: ignore[reportGeneralTypeIssues]
        "w:h", ST_TwipsMeasure
    )
    orient: WD_ORIENTATION = (
        OptionalAttribute(  # pyright: ignore[reportGeneralTypeIssues]
            "w:orient", WD_ORIENTATION, default=WD_ORIENTATION.PORTRAIT
        )
    )


class CT_SectPr(BaseOxmlElement):
    """`w:sectPr` element, the container element for section properties."""

    get_or_add_pgMar: Callable[[], CT_PageMar]
    get_or_add_pgSz: Callable[[], CT_PageSz]
    get_or_add_titlePg: Callable[[], CT_OnOff]
    get_or_add_type: Callable[[], CT_SectType]
    _add_footerReference: Callable[[], CT_HdrFtrRef]
    _add_headerReference: Callable[[], CT_HdrFtrRef]
    _remove_titlePg: Callable[[], None]
    _remove_type: Callable[[], None]

    _tag_seq = (
        "w:footnotePr",
        "w:endnotePr",
        "w:type",
        "w:pgSz",
        "w:pgMar",
        "w:paperSrc",
        "w:pgBorders",
        "w:lnNumType",
        "w:pgNumType",
        "w:cols",
        "w:formProt",
        "w:vAlign",
        "w:noEndnote",
        "w:titlePg",
        "w:textDirection",
        "w:bidi",
        "w:rtlGutter",
        "w:docGrid",
        "w:printerSettings",
        "w:sectPrChange",
    )
    headerReference = ZeroOrMore("w:headerReference", successors=_tag_seq)
    footerReference = ZeroOrMore("w:footerReference", successors=_tag_seq)
    type: CT_SectType | None = ZeroOrOne(  # pyright: ignore[reportGeneralTypeIssues]
        "w:type", successors=_tag_seq[3:]
    )
    pgSz: CT_PageSz | None = ZeroOrOne(  # pyright: ignore[reportGeneralTypeIssues]
        "w:pgSz", successors=_tag_seq[4:]
    )
    pgMar: CT_PageMar | None = ZeroOrOne(  # pyright: ignore[reportGeneralTypeIssues]
        "w:pgMar", successors=_tag_seq[5:]
    )
    titlePg: CT_OnOff | None = ZeroOrOne(  # pyright: ignore[reportGeneralTypeIssues]
        "w:titlePg", successors=_tag_seq[14:]
    )
    del _tag_seq

    def add_footerReference(self, type_: WD_HEADER_FOOTER, rId: str) -> CT_HdrFtrRef:
        """Return newly added CT_HdrFtrRef element of `type_` with `rId`.

        The element tag is `w:footerReference`.
        """
        footerReference = self._add_footerReference()
        footerReference.type_ = type_
        footerReference.rId = rId
        return footerReference

    def add_headerReference(self, type_: WD_HEADER_FOOTER, rId: str) -> CT_HdrFtrRef:
        """Return newly added CT_HdrFtrRef element of `type_` with `rId`.

        The element tag is `w:headerReference`.
        """
        headerReference = self._add_headerReference()
        headerReference.type_ = type_
        headerReference.rId = rId
        return headerReference

    @property
    def bottom_margin(self) -> Length | None:
        """Value of the `w:bottom` attr of `<w:pgMar>` child element, as |Length|.

        |None| when either the element or the attribute is not present.
        """
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.bottom

    @bottom_margin.setter
    def bottom_margin(self, value: int | Length | None):
        pgMar = self.get_or_add_pgMar()
        pgMar.bottom = (
            value if value is None or isinstance(value, Length) else Length(value)
        )

    def clone(self) -> CT_SectPr:
        """Return an exact duplicate of this ``<w:sectPr>`` element tree suitable for
        use in adding a section break.

        All rsid* attributes are removed from the root ``<w:sectPr>`` element.
        """
        cloned_sectPr = deepcopy(self)
        cloned_sectPr.attrib.clear()
        return cloned_sectPr

    @property
    def footer(self) -> Length | None:
        """Distance from bottom edge of page to bottom edge of the footer.

        This is the value of the `w:footer` attribute in the `w:pgMar` child element,
        as a |Length| object, or |None| if either the element or the attribute is not
        present.
        """
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.footer

    @footer.setter
    def footer(self, value: int | Length | None):
        pgMar = self.get_or_add_pgMar()
        pgMar.footer = (
            value if value is None or isinstance(value, Length) else Length(value)
        )

    def get_footerReference(self, type_: WD_HEADER_FOOTER) -> CT_HdrFtrRef | None:
        """Return footerReference element of `type_` or None if not present."""
        path = "./w:footerReference[@w:type='%s']" % WD_HEADER_FOOTER.to_xml(type_)
        footerReferences = self.xpath(path)
        if not footerReferences:
            return None
        return footerReferences[0]

    def get_headerReference(self, type_: WD_HEADER_FOOTER) -> CT_HdrFtrRef | None:
        """Return headerReference element of `type_` or None if not present."""
        matching_headerReferences = self.xpath(
            "./w:headerReference[@w:type='%s']" % WD_HEADER_FOOTER.to_xml(type_)
        )
        if len(matching_headerReferences) == 0:
            return None
        return matching_headerReferences[0]

    @property
    def gutter(self) -> Length | None:
        """The value of the ``w:gutter`` attribute in the ``<w:pgMar>`` child element,
        as a |Length| object, or |None| if either the element or the attribute is not
        present."""
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.gutter

    @gutter.setter
    def gutter(self, value: int | Length | None):
        pgMar = self.get_or_add_pgMar()
        pgMar.gutter = (
            value if value is None or isinstance(value, Length) else Length(value)
        )

    @property
    def header(self) -> Length | None:
        """Distance from top edge of page to top edge of header.

        This value comes from the `w:header` attribute on the `w:pgMar` child element.
        |None| if either the element or the attribute is not present.
        """
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.header

    @header.setter
    def header(self, value: int | Length | None):
        pgMar = self.get_or_add_pgMar()
        pgMar.header = (
            value if value is None or isinstance(value, Length) else Length(value)
        )

    def iter_inner_content(self) -> Iterator[CT_P | CT_Tbl]:
        """Generate all `w:p` and `w:tbl` elements in this section.

        Elements appear in document order. Elements shaded by nesting in a `w:ins` or
        other "wrapper" element will not be included.
        """
        return _SectBlockElementIterator.iter_sect_block_elements(self)

    @property
    def left_margin(self) -> Length | None:
        """The value of the ``w:left`` attribute in the ``<w:pgMar>`` child element, as
        a |Length| object, or |None| if either the element or the attribute is not
        present."""
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.left

    @left_margin.setter
    def left_margin(self, value: int | Length | None):
        pgMar = self.get_or_add_pgMar()
        pgMar.left = (
            value if value is None or isinstance(value, Length) else Length(value)
        )

    @property
    def orientation(self) -> WD_ORIENTATION:
        """`WD_ORIENTATION` member indicating page-orientation for this section.

        This is the value of the `orient` attribute on the `w:pgSz` child, or
        `WD_ORIENTATION.PORTRAIT` if not present.
        """
        pgSz = self.pgSz
        if pgSz is None:
            return WD_ORIENTATION.PORTRAIT
        return pgSz.orient

    @orientation.setter
    def orientation(self, value: WD_ORIENTATION | None):
        pgSz = self.get_or_add_pgSz()
        pgSz.orient = value if value else WD_ORIENTATION.PORTRAIT

    @property
    def page_height(self) -> Length | None:
        """Value in EMU of the `h` attribute of the `w:pgSz` child element.

        |None| if not present.
        """
        pgSz = self.pgSz
        if pgSz is None:
            return None
        return pgSz.h

    @page_height.setter
    def page_height(self, value: Length | None):
        pgSz = self.get_or_add_pgSz()
        pgSz.h = value

    @property
    def page_width(self) -> Length | None:
        """Value in EMU of the ``w`` attribute of the ``<w:pgSz>`` child element.

        |None| if not present.
        """
        pgSz = self.pgSz
        if pgSz is None:
            return None
        return pgSz.w

    @page_width.setter
    def page_width(self, value: Length | None):
        pgSz = self.get_or_add_pgSz()
        pgSz.w = value

    @property
    def preceding_sectPr(self) -> CT_SectPr | None:
        """SectPr immediately preceding this one or None if this is the first."""
        # -- [1] predicate returns list of zero or one value --
        preceding_sectPrs = self.xpath("./preceding::w:sectPr[1]")
        return preceding_sectPrs[0] if len(preceding_sectPrs) > 0 else None

    def remove_footerReference(self, type_: WD_HEADER_FOOTER) -> str:
        """Return rId of w:footerReference child of `type_` after removing it."""
        footerReference = self.get_footerReference(type_)
        if footerReference is None:
            # -- should never happen, but to satisfy type-check and just in case --
            raise ValueError("CT_SectPr has no footer reference")
        rId = footerReference.rId
        self.remove(footerReference)
        return rId

    def remove_headerReference(self, type_: WD_HEADER_FOOTER):
        """Return rId of w:headerReference child of `type_` after removing it."""
        headerReference = self.get_headerReference(type_)
        if headerReference is None:
            # -- should never happen, but to satisfy type-check and just in case --
            raise ValueError("CT_SectPr has no header reference")
        rId = headerReference.rId
        self.remove(headerReference)
        return rId

    @property
    def right_margin(self) -> Length | None:
        """The value of the ``w:right`` attribute in the ``<w:pgMar>`` child element, as
        a |Length| object, or |None| if either the element or the attribute is not
        present."""
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.right

    @right_margin.setter
    def right_margin(self, value: Length | None):
        pgMar = self.get_or_add_pgMar()
        pgMar.right = value

    @property
    def start_type(self) -> WD_SECTION_START:
        """The member of the ``WD_SECTION_START`` enumeration corresponding to the value
        of the ``val`` attribute of the ``<w:type>`` child element, or
        ``WD_SECTION_START.NEW_PAGE`` if not present."""
        type = self.type
        if type is None or type.val is None:
            return WD_SECTION_START.NEW_PAGE
        return type.val

    @start_type.setter
    def start_type(self, value: WD_SECTION_START | None):
        if value is None or value is WD_SECTION_START.NEW_PAGE:
            self._remove_type()
            return
        type = self.get_or_add_type()
        type.val = value

    @property
    def titlePg_val(self) -> bool:
        """Value of `w:titlePg/@val` or |False| if `./w:titlePg` is not present."""
        titlePg = self.titlePg
        if titlePg is None:
            return False
        return titlePg.val

    @titlePg_val.setter
    def titlePg_val(self, value: bool | None):
        if value in [None, False]:
            self._remove_titlePg()
        else:
            self.get_or_add_titlePg().val = True

    @property
    def top_margin(self) -> Length | None:
        """The value of the ``w:top`` attribute in the ``<w:pgMar>`` child element, as a
        |Length| object, or |None| if either the element or the attribute is not
        present."""
        pgMar = self.pgMar
        if pgMar is None:
            return None
        return pgMar.top

    @top_margin.setter
    def top_margin(self, value: Length | None):
        pgMar = self.get_or_add_pgMar()
        pgMar.top = value


class CT_SectType(BaseOxmlElement):
    """``<w:sectType>`` element, defining the section start type."""

    val: WD_SECTION_START | None = (  # pyright: ignore[reportGeneralTypeIssues]
        OptionalAttribute("w:val", WD_SECTION_START)
    )


# == HELPERS =========================================================================


class _SectBlockElementIterator:
    """Generates the block-item XML elements in a section.

    A block-item element is a `CT_P` (paragraph) or a `CT_Tbl` (table).
    """

    _compiled_blocks_xpath: etree.XPath | None = None
    _compiled_count_xpath: etree.XPath | None = None

    def __init__(self, sectPr: CT_SectPr):
        self._sectPr = sectPr

    @classmethod
    def iter_sect_block_elements(cls, sectPr: CT_SectPr) -> Iterator[BlockElement]:
        """Generate each CT_P or CT_Tbl element within extents governed by `sectPr`."""
        return cls(sectPr)._iter_sect_block_elements()

    def _iter_sect_block_elements(self) -> Iterator[BlockElement]:
        """Generate each CT_P or CT_Tbl element in section."""
        # -- General strategy is to get all block (<w;p> and <w:tbl>) elements from
        # -- start of doc to and including this section, then compute the count of those
        # -- elements that came from prior sections and skip that many to leave only the
        # -- ones in this section. It's possible to express this "between here and
        # -- there" (end of prior section and end of this one) concept in XPath, but it
        # -- would be harder to follow because there are special cases (e.g. no prior
        # -- section) and the boundary expressions are fairly hairy. I also believe it
        # -- would be computationally more expensive than doing it this straighforward
        # -- albeit (theoretically) slightly wasteful way.

        sectPr, sectPrs = self._sectPr, self._sectPrs
        sectPr_idx = sectPrs.index(sectPr)

        # -- count block items belonging to prior sections --
        n_blks_to_skip = (
            0
            if sectPr_idx == 0
            else self._count_of_blocks_in_and_above_section(sectPrs[sectPr_idx - 1])
        )

        # -- and skip those in set of all blks from doc start to end of this section --
        for element in self._blocks_in_and_above_section(sectPr)[n_blks_to_skip:]:
            yield element

    def _blocks_in_and_above_section(self, sectPr: CT_SectPr) -> Sequence[BlockElement]:
        """All ps and tbls in section defined by `sectPr` and all prior sections."""
        if self._compiled_blocks_xpath is None:
            self._compiled_blocks_xpath = etree.XPath(
                self._blocks_in_and_above_section_xpath,
                namespaces=nsmap,
                regexp=False,
            )
        xpath = self._compiled_blocks_xpath
        # -- XPath callable results are Any (basically), so need a cast. Also the
        # -- callable wants an etree._Element, which CT_SectPr is, but we haven't
        # -- figured out the typing through the metaclass yet.
        return cast(
            Sequence[BlockElement],
            xpath(sectPr),  # pyright: ignore[reportGeneralTypeIssues]
        )

    @lazyproperty
    def _blocks_in_and_above_section_xpath(self) -> str:
        """XPath expr for ps and tbls in context of a sectPr and all prior sectPrs."""
        # -- "p_sect" is a section with sectPr located at w:p/w:pPr/w:sectPr.
        # -- "body_sect" is a section with sectPr located at w:body/w:sectPr. The last
        # -- section in the document is a "body_sect". All others are of the "p_sect"
        # -- variety. "term" means "terminal", like the last p or tbl in the section.
        # -- "pred" means "predecessor", like a preceding p or tbl in the section.

        # -- the terminal block in a p-based sect is the p the sectPr appears in --
        p_sect_term_block = "./parent::w:pPr/parent::w:p"
        # -- the terminus of a body-based sect is the sectPr itself (not a block) --
        body_sect_term = "self::w:sectPr[parent::w:body]"
        # -- all the ps and tbls preceding (but not including) the context node --
        pred_ps_and_tbls = "preceding-sibling::*[self::w:p | self::w:tbl]"

        # -- p_sect_term_block and body_sect_term(inus) are mutually exclusive. So the
        # -- result is either the union of nodes found by the first two selectors or the
        # -- nodes found by the last selector, never both.
        return (
            # -- include the p containing a sectPr --
            f"{p_sect_term_block}"
            # -- along with all the blocks that precede it --
            f" | {p_sect_term_block}/{pred_ps_and_tbls}"
            # -- or all the preceding blocks if sectPr is body-based (last sectPr) --
            f" | {body_sect_term}/{pred_ps_and_tbls}"
        )

    def _count_of_blocks_in_and_above_section(self, sectPr: CT_SectPr) -> int:
        """All ps and tbls in section defined by `sectPr` and all prior sections."""
        if self._compiled_count_xpath is None:
            self._compiled_count_xpath = etree.XPath(
                f"count({self._blocks_in_and_above_section_xpath})",
                namespaces=nsmap,
                regexp=False,
            )
        xpath = self._compiled_count_xpath
        # -- numeric XPath results are always float, so need an int() conversion --
        return int(
            cast(float, xpath(sectPr))  # pyright: ignore[reportGeneralTypeIssues]
        )

    @lazyproperty
    def _sectPrs(self) -> Sequence[CT_SectPr]:
        """All w:sectPr elements in document, in document-order."""
        return self._sectPr.xpath(
            "/w:document/w:body/w:p/w:pPr/w:sectPr | /w:document/w:body/w:sectPr",
        )
