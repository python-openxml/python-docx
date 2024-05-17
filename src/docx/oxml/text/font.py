"""Custom element classes related to run properties (font)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from docx.enum.dml import MSO_THEME_COLOR
from docx.enum.text import WD_COLOR_INDEX, WD_UNDERLINE
from docx.oxml.ns import nsdecls
from docx.oxml.parser import parse_xml
from docx.oxml.simpletypes import (
    ST_HexColor,
    ST_HpsMeasure,
    ST_String,
    ST_VerticalAlignRun,
)
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OptionalAttribute,
    RequiredAttribute,
    ZeroOrOne,
)

if TYPE_CHECKING:
    from docx.oxml.shared import CT_OnOff, CT_String
    from docx.shared import Length


class CT_Color(BaseOxmlElement):
    """`w:color` element, specifying the color of a font and perhaps other objects."""

    val = RequiredAttribute("w:val", ST_HexColor)
    themeColor = OptionalAttribute("w:themeColor", MSO_THEME_COLOR)


class CT_Fonts(BaseOxmlElement):
    """`<w:rFonts>` element.

    Specifies typeface name for the various language types.
    """

    ascii: str | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:ascii", ST_String
    )
    hAnsi: str | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:hAnsi", ST_String
    )


class CT_Highlight(BaseOxmlElement):
    """`w:highlight` element, specifying font highlighting/background color."""

    val: WD_COLOR_INDEX = RequiredAttribute(  # pyright: ignore[reportGeneralTypeIssues]
        "w:val", WD_COLOR_INDEX
    )


class CT_HpsMeasure(BaseOxmlElement):
    """Used for `<w:sz>` element and others, specifying font size in half-points."""

    val: Length = RequiredAttribute(  # pyright: ignore[reportGeneralTypeIssues]
        "w:val", ST_HpsMeasure
    )


class CT_RPr(BaseOxmlElement):
    """`<w:rPr>` element, containing the properties for a run."""

    get_or_add_highlight: Callable[[], CT_Highlight]
    get_or_add_rFonts: Callable[[], CT_Fonts]
    get_or_add_sz: Callable[[], CT_HpsMeasure]
    get_or_add_vertAlign: Callable[[], CT_VerticalAlignRun]
    _add_rStyle: Callable[..., CT_String]
    _add_u: Callable[[], CT_Underline]
    _remove_highlight: Callable[[], None]
    _remove_rFonts: Callable[[], None]
    _remove_rStyle: Callable[[], None]
    _remove_sz: Callable[[], None]
    _remove_u: Callable[[], None]
    _remove_vertAlign: Callable[[], None]

    _tag_seq = (
        "w:rStyle",
        "w:rFonts",
        "w:b",
        "w:bCs",
        "w:i",
        "w:iCs",
        "w:caps",
        "w:smallCaps",
        "w:strike",
        "w:dstrike",
        "w:outline",
        "w:shadow",
        "w:emboss",
        "w:imprint",
        "w:noProof",
        "w:snapToGrid",
        "w:vanish",
        "w:webHidden",
        "w:color",
        "w:spacing",
        "w:w",
        "w:kern",
        "w:position",
        "w:sz",
        "w:szCs",
        "w:highlight",
        "w:u",
        "w:effect",
        "w:bdr",
        "w:shd",
        "w:fitText",
        "w:vertAlign",
        "w:rtl",
        "w:cs",
        "w:em",
        "w:lang",
        "w:eastAsianLayout",
        "w:specVanish",
        "w:oMath",
    )
    rStyle: CT_String | None = ZeroOrOne(  # pyright: ignore[reportGeneralTypeIssues]
        "w:rStyle", successors=_tag_seq[1:]
    )
    rFonts: CT_Fonts | None = ZeroOrOne(  # pyright: ignore[reportGeneralTypeIssues]
        "w:rFonts", successors=_tag_seq[2:]
    )
    b: CT_OnOff | None = ZeroOrOne(  # pyright: ignore[reportGeneralTypeIssues]
        "w:b", successors=_tag_seq[3:]
    )
    bCs = ZeroOrOne("w:bCs", successors=_tag_seq[4:])
    i = ZeroOrOne("w:i", successors=_tag_seq[5:])
    iCs = ZeroOrOne("w:iCs", successors=_tag_seq[6:])
    caps = ZeroOrOne("w:caps", successors=_tag_seq[7:])
    smallCaps = ZeroOrOne("w:smallCaps", successors=_tag_seq[8:])
    strike = ZeroOrOne("w:strike", successors=_tag_seq[9:])
    dstrike = ZeroOrOne("w:dstrike", successors=_tag_seq[10:])
    outline = ZeroOrOne("w:outline", successors=_tag_seq[11:])
    shadow = ZeroOrOne("w:shadow", successors=_tag_seq[12:])
    emboss = ZeroOrOne("w:emboss", successors=_tag_seq[13:])
    imprint = ZeroOrOne("w:imprint", successors=_tag_seq[14:])
    noProof = ZeroOrOne("w:noProof", successors=_tag_seq[15:])
    snapToGrid = ZeroOrOne("w:snapToGrid", successors=_tag_seq[16:])
    vanish = ZeroOrOne("w:vanish", successors=_tag_seq[17:])
    webHidden = ZeroOrOne("w:webHidden", successors=_tag_seq[18:])
    color = ZeroOrOne("w:color", successors=_tag_seq[19:])
    sz: CT_HpsMeasure | None = ZeroOrOne(  # pyright: ignore[reportGeneralTypeIssues]
        "w:sz", successors=_tag_seq[24:]
    )
    highlight: CT_Highlight | None = ZeroOrOne(  # pyright: ignore[reportGeneralTypeIssues]
        "w:highlight", successors=_tag_seq[26:]
    )
    u: CT_Underline | None = ZeroOrOne(  # pyright: ignore[reportGeneralTypeIssues]
        "w:u", successors=_tag_seq[27:]
    )
    vertAlign: CT_VerticalAlignRun | None = ZeroOrOne(  # pyright: ignore[reportGeneralTypeIssues]
        "w:vertAlign", successors=_tag_seq[32:]
    )
    rtl = ZeroOrOne("w:rtl", successors=_tag_seq[33:])
    cs = ZeroOrOne("w:cs", successors=_tag_seq[34:])
    specVanish = ZeroOrOne("w:specVanish", successors=_tag_seq[38:])
    oMath = ZeroOrOne("w:oMath", successors=_tag_seq[39:])
    del _tag_seq

    def _new_color(self):
        """Override metaclass method to set `w:color/@val` to RGB black on create."""
        return parse_xml('<w:color %s w:val="000000"/>' % nsdecls("w"))

    @property
    def highlight_val(self) -> WD_COLOR_INDEX | None:
        """Value of `./w:highlight/@val`.

        Specifies font's highlight color, or `None` if the text is not highlighted.
        """
        highlight = self.highlight
        if highlight is None:
            return None
        return highlight.val

    @highlight_val.setter
    def highlight_val(self, value: WD_COLOR_INDEX | None) -> None:
        if value is None:
            self._remove_highlight()
            return
        highlight = self.get_or_add_highlight()
        highlight.val = value

    @property
    def rFonts_ascii(self) -> str | None:
        """The value of `w:rFonts/@w:ascii` or |None| if not present.

        Represents the assigned typeface name. The rFonts element also specifies other
        special-case typeface names; this method handles the case where just the common
        name is required.
        """
        rFonts = self.rFonts
        if rFonts is None:
            return None
        return rFonts.ascii

    @rFonts_ascii.setter
    def rFonts_ascii(self, value: str | None) -> None:
        if value is None:
            self._remove_rFonts()
            return
        rFonts = self.get_or_add_rFonts()
        rFonts.ascii = value

    @property
    def rFonts_hAnsi(self) -> str | None:
        """The value of `w:rFonts/@w:hAnsi` or |None| if not present."""
        rFonts = self.rFonts
        if rFonts is None:
            return None
        return rFonts.hAnsi

    @rFonts_hAnsi.setter
    def rFonts_hAnsi(self, value: str | None):
        if value is None and self.rFonts is None:
            return
        rFonts = self.get_or_add_rFonts()
        rFonts.hAnsi = value

    @property
    def style(self) -> str | None:
        """String in `./w:rStyle/@val`, or None if `w:rStyle` is not present."""
        rStyle = self.rStyle
        if rStyle is None:
            return None
        return rStyle.val

    @style.setter
    def style(self, style: str | None) -> None:
        """Set `./w:rStyle/@val` to `style`, adding the `w:rStyle` element if necessary.

        If `style` is |None|, remove `w:rStyle` element if present.
        """
        if style is None:
            self._remove_rStyle()
        elif self.rStyle is None:
            self._add_rStyle(val=style)
        else:
            self.rStyle.val = style

    @property
    def subscript(self) -> bool | None:
        """|True| if `./w:vertAlign/@w:val` is "subscript".

        |False| if `w:vertAlign/@w:val` contains any other value. |None| if
        `w:vertAlign` is not present.
        """
        vertAlign = self.vertAlign
        if vertAlign is None:
            return None
        if vertAlign.val == ST_VerticalAlignRun.SUBSCRIPT:
            return True
        return False

    @subscript.setter
    def subscript(self, value: bool | None) -> None:
        if value is None:
            self._remove_vertAlign()
        elif bool(value) is True:
            self.get_or_add_vertAlign().val = ST_VerticalAlignRun.SUBSCRIPT
        # -- assert bool(value) is False --
        elif self.vertAlign is not None and self.vertAlign.val == ST_VerticalAlignRun.SUBSCRIPT:
            self._remove_vertAlign()

    @property
    def superscript(self) -> bool | None:
        """|True| if `w:vertAlign/@w:val` is 'superscript'.

        |False| if `w:vertAlign/@w:val` contains any other value. |None| if
        `w:vertAlign` is not present.
        """
        vertAlign = self.vertAlign
        if vertAlign is None:
            return None
        if vertAlign.val == ST_VerticalAlignRun.SUPERSCRIPT:
            return True
        return False

    @superscript.setter
    def superscript(self, value: bool | None):
        if value is None:
            self._remove_vertAlign()
        elif bool(value) is True:
            self.get_or_add_vertAlign().val = ST_VerticalAlignRun.SUPERSCRIPT
        # -- assert bool(value) is False --
        elif self.vertAlign is not None and self.vertAlign.val == ST_VerticalAlignRun.SUPERSCRIPT:
            self._remove_vertAlign()

    @property
    def sz_val(self) -> Length | None:
        """The value of `w:sz/@w:val` or |None| if not present."""
        sz = self.sz
        if sz is None:
            return None
        return sz.val

    @sz_val.setter
    def sz_val(self, value: Length | None):
        if value is None:
            self._remove_sz()
            return
        sz = self.get_or_add_sz()
        sz.val = value

    @property
    def u_val(self) -> WD_UNDERLINE | None:
        """Value of `w:u/@val`, or None if not present.

        Values `WD_UNDERLINE.SINGLE` and `WD_UNDERLINE.NONE` are mapped to `True` and
        `False` respectively.
        """
        u = self.u
        if u is None:
            return None
        return u.val

    @u_val.setter
    def u_val(self, value: WD_UNDERLINE | None):
        self._remove_u()
        if value is not None:
            self._add_u().val = value

    def _get_bool_val(self, name: str) -> bool | None:
        """Value of boolean child with `name`, e.g. "w:b", "w:i", and "w:smallCaps"."""
        element = getattr(self, name)
        if element is None:
            return None
        return element.val

    def _set_bool_val(self, name: str, value: bool | None):
        if value is None:
            getattr(self, "_remove_%s" % name)()
            return
        element = getattr(self, "get_or_add_%s" % name)()
        element.val = value


class CT_Underline(BaseOxmlElement):
    """`<w:u>` element, specifying the underlining style for a run."""

    val: WD_UNDERLINE | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:val", WD_UNDERLINE
    )


class CT_VerticalAlignRun(BaseOxmlElement):
    """`<w:vertAlign>` element, specifying subscript or superscript."""

    val: str = RequiredAttribute(  # pyright: ignore[reportGeneralTypeIssues]
        "w:val", ST_VerticalAlignRun
    )
