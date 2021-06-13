# encoding: utf-8

"""Custom element classes for textboxed"""

from docx.oxml.text import paragraph
from ..blkcntnr import BlockItemContainer
from ..shared import ElementProxy
from .simpletypes import XsdUnsignedInt, XsdString
from .xmlchemy import (
    BaseOxmlElement,
    OneAndOnlyOne,
    OneOrMore,
    RequiredAttribute,
    ZeroOrMore,
    ZeroOrOne,
)

XPATH_CHOICE = "./mc:Choice/w:drawing/wp:anchor/a:graphic/a:graphicData/wps:wsp/wps:txbx\
    /w:txbxContent"
XPATH_FALLBACK = "./mc:Fallback/w:pict/v:*/v:textbox/w:txbxContent"


class CT_TextBoxContent(BaseOxmlElement):
    """
    ``<w:txbxContent>`` element
    """

    p = ZeroOrMore("w:p")


class CT_LinkedTextboxInformation(BaseOxmlElement):
    """
    ``<wps:linkedTxbx>`` element
    """

    identifier = RequiredAttribute("id", XsdUnsignedInt)
    seq = RequiredAttribute("seq", XsdUnsignedInt)


class CT_TextboxInfo(BaseOxmlElement):
    """
    ``<wps:txbx>`` element
    """

    txbxContent = OneAndOnlyOne("w:txbxContent")


class CT_WordprocessingShape(BaseOxmlElement):
    """
    ``<wps:wsp>`` element
    """

    txbx = ZeroOrOne("wps:txbx")


class Anchor(BaseOxmlElement):
    """
    ``<wp:anchor>`` element
    """

    # I think there has to be exactly one, not sure
    graphic = ZeroOrMore("a:graphic")


class TextBox(ElementProxy):
    """Text box class that stores two TextBoxContent objects

    The reason why it needs to store two textboxes is because two copies with different
    formatting are stored in the document for legacy reasons.
    """

    def __init__(self, element):
        """
        Initialize using an ``<mc:AlternateContent>`` object
        """
        super(TextBox, self).__init__(element)

        try:
            (tbox1,) = element.xpath(XPATH_CHOICE)
            (tbox2,) = element.xpath(XPATH_FALLBACK)
        except ValueError as err:
            raise ValueError(
                "This element is not a text box; it should contain precisely two \
                    ``<w:txbxContent>`` objects"
            )
        self.tbox1 = TextBoxContent(tbox1, self)
        self.tbox2 = TextBoxContent(tbox2, self)

    def add_paragraph(self, text="", style=None):
        paragraph = self.tbox1.add_paragraph(text=text, style=style)
        _ = self.tbox2.add_paragraph(text=text, style=style)
        return paragraph

    def add_table(self, rows, cols, width):
        tbl = self.tbox1.add_table(rows, cols, width)
        _ = self.tbox2.add_table(rows, cols, width)
        return tbl

    @property
    def paragraphs(self):
        return self.tbox1.paragraphs

    @property
    def tables(self):
        return self.tbox1.tables

    @property
    def text(self):
        return "\n".join(p.text for p in self.paragraphs)

    @text.setter
    def text(self, text):
        for tbox in [self.tbox1, self.tbox2]:
            tbox.clear_content()
            p = tbox._add_paragraph()
            r = p.add_run()
            r.text = text

    def clear_content(self):
        self.tbox1.clear_content()
        self.tbox2.clear_content()


class TextBoxContent(BlockItemContainer):
    def clear_content(self):
        for c in self._element[:]:
            self._element.remove(c)


class AlternateContentChoice(BaseOxmlElement):
    """
    ``<mc:Choice>`` element
    """

    requires = RequiredAttribute("Requires", XsdString)


class AlternateContentFallback(BaseOxmlElement):
    """
    ``<mc:Fallback>`` element
    """


class AlternateContent(BaseOxmlElement):
    """
    ``<mc:AlternateContent>`` element
    """

    choice = OneOrMore("mc:AlternateChoice")
    fallback = OneOrMore("mc:Fallback")


def find_textboxes(element):
    """
    List all text box objects in the document.

    Looks for all ``<mc:AlternateContent>`` elements, and selects those
    which contain a text box. 
    """
    alt_cont_elems = element.xpath(".//mc:AlternateContent")
    text_boxes = []
    for elem in alt_cont_elems:
        tbox1 = elem.xpath(XPATH_CHOICE)
        tbox2 = elem.xpath(XPATH_FALLBACK)
        if len(tbox1) == 1 and len(tbox2) == 1:
            text_boxes.append(TextBox(elem))
    return text_boxes
