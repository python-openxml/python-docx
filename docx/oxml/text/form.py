# encoding: utf-8
"""
Implementation of the following forms elements

FORMCHECKBOX (§17.16.5.20),
FORMDROPDOWN (§17.16.5.21),
FORMTEXT (§17.16.5.22)
"""

from ..simpletypes import XsdString, ST_OnOff, XsdStringEnumeration
from ..xmlchemy import (
    BaseOxmlElement,
    OptionalAttribute,
    RequiredAttribute,
    OneOrMore,
    ZeroOrOne,
)


class CT_SimpleField(BaseOxmlElement):
    """
    ``<w:simplefield>`` element
    """

    fldLock = OptionalAttribute("w:fldLock", ST_OnOff)
    dirty = OptionalAttribute("w:dirty", ST_OnOff)
    instr = OptionalAttribute("w:instr", XsdString)


class ST_FldCharType(XsdStringEnumeration):
    """
    Valid values for <w:fldChar fldCharType=""> attribute
    """

    BEGIN = "begin"
    SEPARATE = "separate"
    END = "end"
    _members = (BEGIN, SEPARATE, END)


class CT_FldChar(BaseOxmlElement):
    """
    The ``<w:fldchar">`` element
    """

    ffData = ZeroOrOne("w:ffData")
    fldCharType = RequiredAttribute("w:fldCharType", ST_FldCharType)
    fldLock = OptionalAttribute("w:fldLock", ST_OnOff)
    dirty = OptionalAttribute("w:dirty", ST_OnOff)


class CT_FFData(BaseOxmlElement):
    """
    The ``<w:ffData">`` element
    """

    name = ZeroOrOne("w:name")
    label = ZeroOrOne("w:label")
    tabIndex = ZeroOrOne("w:tabIndex")
    enabled = ZeroOrOne("w:enabled")
    calcOnExit = ZeroOrOne("w:calcOnExit")
    entryMacro = ZeroOrOne("w:entryMacro")
    exitMacro = ZeroOrOne("w:exitMacro")
    helpText = ZeroOrOne("w:helpText")
    statusText = ZeroOrOne("w:statusText")
    checkBox = ZeroOrOne("w:checkBox")
    ddList = ZeroOrOne("w:ddList")
    textInput = ZeroOrOne("w:textInput")


class CT_FFDDList(BaseOxmlElement):
    """
    The ``<w:ffddlist">`` element.
    """

    default = ZeroOrOne("w:default")
    result = ZeroOrOne("w:result")
    listEntry = OneOrMore("w:listEntry")


class CT_FFCheckBox(BaseOxmlElement):  # noqa
    """
    The ``FFCheckBox`` element.
    """

    checked = ZeroOrOne("w:checked")
    default = ZeroOrOne("w:default")


class CT_FFTextInput(BaseOxmlElement):  # noqa
    """
    The ''<w:textinput>'' element
    """

    type_ = ZeroOrOne("w:type")
    default = ZeroOrOne("w:default")
    format_ = ZeroOrOne("w:format")


class ST_FFTextType(XsdStringEnumeration):
    """
    The ``fldCharType`` attribute of <w:fldChar> elements
    """

    REGULAR = "regular"
    NUMBER = "number"
    DATE = "date"
    CURRENTTIME = "currentTime"
    CURRENTDATE = "currentDate"
    CALCULATED = "calculated"
    _members = (REGULAR, NUMBER, DATE, CURRENTTIME, CURRENTDATE, CALCULATED)


class CT_FFTextType(BaseOxmlElement):  # noqa
    """
    Used for ``<w:pStyle>`` and ``<w:tblStyle>`` elements and others,
    containing a style name in its ``val`` attribute.
    """

    val = RequiredAttribute("w:val", ST_FFTextType)
