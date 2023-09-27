"""Custom element classes related to text runs (CT_R)."""

from __future__ import annotations

from docx.oxml.ns import qn
from docx.oxml.simpletypes import ST_BrClear, ST_BrType
from docx.oxml.xmlchemy import BaseOxmlElement, OptionalAttribute, ZeroOrMore, ZeroOrOne

# ------------------------------------------------------------------------------------
# Run-level elements


class CT_R(BaseOxmlElement):
    """`<w:r>` element, containing the properties and text for a run."""

    rPr = ZeroOrOne("w:rPr")
    t = ZeroOrMore("w:t")
    br = ZeroOrMore("w:br")
    cr = ZeroOrMore("w:cr")
    tab = ZeroOrMore("w:tab")
    drawing = ZeroOrMore("w:drawing")

    def add_t(self, text: str) -> CT_Text:
        """Return a newly added `<w:t>` element containing `text`."""
        t = self._add_t(text=text)
        if len(text.strip()) < len(text):
            t.set(qn("xml:space"), "preserve")
        return t

    def add_drawing(self, inline_or_anchor):
        """Return newly appended `CT_Drawing` (`w:drawing`) child element.

        The `w:drawing` element has `inline_or_anchor` as its child.
        """
        drawing = self._add_drawing()
        drawing.append(inline_or_anchor)
        return drawing

    def clear_content(self):
        """Remove all child elements except a `w:rPr` element if present."""
        content_child_elms = self[1:] if self.rPr is not None else self[:]
        for child in content_child_elms:
            self.remove(child)

    @property
    def style(self):
        """String contained in `w:val` attribute of `w:rStyle` grandchild.

        |None| if that element is not present.
        """
        rPr = self.rPr
        if rPr is None:
            return None
        return rPr.style

    @style.setter
    def style(self, style):
        """Set character style of this `w:r` element to `style`.

        If `style` is None, remove the style element.
        """
        rPr = self.get_or_add_rPr()
        rPr.style = style

    @property
    def text(self):
        """The textual content of this run.

        Inner-content child elements like `w:tab` are translated to their text
        equivalent.
        """
        text = ""
        for child in self:
            if child.tag == qn("w:t"):
                t_text = child.text
                text += t_text if t_text is not None else ""
            elif child.tag == qn("w:tab"):
                text += "\t"
            elif child.tag in (qn("w:br"), qn("w:cr")):
                text += "\n"
        return text

    @text.setter
    def text(self, text):
        self.clear_content()
        _RunContentAppender.append_to_run_from_text(self, text)

    def _insert_rPr(self, rPr):
        self.insert(0, rPr)
        return rPr


# ------------------------------------------------------------------------------------
# Run inner-content elements


class CT_Br(BaseOxmlElement):
    """`<w:br>` element, indicating a line, page, or column break in a run."""

    type = OptionalAttribute("w:type", ST_BrType)
    clear = OptionalAttribute("w:clear", ST_BrClear)


class CT_Text(BaseOxmlElement):
    """`<w:t>` element, containing a sequence of characters within a run."""


# ------------------------------------------------------------------------------------
# Utility


class _RunContentAppender(object):
    """Translates a Python string into run content elements appended in a `w:r` element.

    Contiguous sequences of regular characters are appended in a single `<w:t>` element.
    Each tab character ('\t') causes a `<w:tab/>` element to be appended. Likewise a
    newline or carriage return character ('\n', '\r') causes a `<w:cr>` element to be
    appended.
    """

    def __init__(self, r):
        self._r = r
        self._bfr = []

    @classmethod
    def append_to_run_from_text(cls, r, text):
        """Append inner-content elements for `text` to `r` element."""
        appender = cls(r)
        appender.add_text(text)

    def add_text(self, text):
        """Append inner-content elements for `text` to the `w:r` element."""
        for char in text:
            self.add_char(char)
        self.flush()

    def add_char(self, char):
        """Process next character of input through finite state maching (FSM).

        There are two possible states, buffer pending and not pending, but those are
        hidden behind the `.flush()` method which must be called at the end of text to
        ensure any pending `<w:t>` element is written.
        """
        if char == "\t":
            self.flush()
            self._r.add_tab()
        elif char in "\r\n":
            self.flush()
            self._r.add_br()
        else:
            self._bfr.append(char)

    def flush(self):
        text = "".join(self._bfr)
        if text:
            self._r.add_t(text)
        del self._bfr[:]
