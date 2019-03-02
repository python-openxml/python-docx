"""
Implementation of the following forms elements

FORMCHECKBOX (§17.16.5.20),
FORMDROPDOWN (§17.16.5.21),
FORMTEXT (§17.16.5.22)

"""

from ..simpletypes import XsdUnsignedInt, XsdString, ST_OnOff, XsdStringEnumeration

from ..xmlchemy import (
    BaseOxmlElement, 
    OptionalAttribute, RequiredAttribute, 
    OneAndOnlyOne, OneOrMore, ZeroOrMore, ZeroOrOne, ZeroOrOneChoice
)


# ------------------------------
# Simple Field
# ------------------------------

class CT_SimpleField(BaseOxmlElement):
    """
    17.16.19 fldSimple (Simple Field)

    w_CT_SimpleField =
        attribute w:instr { s_ST_String },
        attribute w:fldLock { s_ST_OnOff }?,
        attribute w:dirty { s_ST_OnOff }?,
        w_EG_PContent*

    <xsd:complexType name="CT_SimpleField">
        <xsd:sequence>
            <xsd:group ref="EG_PContent" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
        <xsd:attribute name="instr" type="s:ST_String" use="required"/>
        <xsd:attribute name="fldLock" type="s:ST_OnOff"/>
        <xsd:attribute name="dirty" type="s:ST_OnOff"/>
    </xsd:complexType>
    """
    fldLock = OptionalAttribute('w:fldLock',ST_OnOff)
    dirty = OptionalAttribute('w:dirty',ST_OnOff)
    instr = OptionalAttribute('w:instr',XsdString)


# ------------------------------
# Complex Field
# ------------------------------

 
class ST_FldCharType(XsdStringEnumeration):
    """
    Valid values for <w:fldChar fldCharType=""> attribute

    <xsd:simpleType name="ST_FldCharType">
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="begin"/>
            <xsd:enumeration value="separate"/>
            <xsd:enumeration value="end"/>
        </xsd:restriction>
    </xsd:simpleType>

    """
    BEGIN = 'begin'
    SEPARATE = 'separate'
    END = 'end'

    _members = (BEGIN, SEPARATE, END)
   

class CT_FldChar(BaseOxmlElement):
    """
    17.16.18 fldChar (Complex Field)

    As well, because a complex field can specify both its field codes and its
    current result within the document, these two items are separated by the
    optional separator character, which defines the end of the field codes and
    the beginning of the field contents. The omission of this character shall
    be used to specify that the contents of the field are entirely field codes
    (i.e. the field has no result).

    <xsd:complexType name="CT_FldChar">
        <xsd:choice>
            <xsd:element name="ffData" type="CT_FFData" minOccurs="0" maxOccurs="1"/>
        </xsd:choice>
        <xsd:attribute name="fldCharType" type="ST_FldCharType" use="required"/>
        <xsd:attribute name="fldLock" type="s:ST_OnOff"/>
        <xsd:attribute name="dirty" type="s:ST_OnOff"/>
    </xsd:complexType>
    """
    ffData = ZeroOrOne("w:ffData")

    fldCharType = RequiredAttribute('w:val', ST_FldCharType)
    fldLock = OptionalAttribute('w:fldLock', ST_OnOff)
    dirty = OptionalAttribute('w:dirty', ST_OnOff)


class CT_FFData(BaseOxmlElement):
    """
    17.16.17 ffData (Form Field Properties)

    <xsd:complexType name="CT_FFData">
        <xsd:choice maxOccurs="unbounded">
            <xsd:element name="name" type="CT_FFName"/>
            <xsd:element name="label" type="CT_DecimalNumber" minOccurs="0"/>
            <xsd:element name="tabIndex" type="CT_UnsignedDecimalNumber" minOccurs="0"/>
            <xsd:element name="enabled" type="CT_OnOff"/>
            <xsd:element name="calcOnExit" type="CT_OnOff"/>
            <xsd:element name="entryMacro" type="CT_MacroName" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="exitMacro" type="CT_MacroName" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="helpText" type="CT_FFHelpText" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="statusText" type="CT_FFStatusText" minOccurs="0" maxOccurs="1"/>
            <xsd:choice>
                <xsd:element name="checkBox" type="CT_FFCheckBox"/>
                <xsd:element name="ddList" type="CT_FFDDList"/>
                <xsd:element name="textInput" type="CT_FFTextInput"/>
            </xsd:choice>
        </xsd:choice>
    </xsd:complexType>
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

# ------------------------------
# Drop Down List
# ------------------------------

class CT_FFDDList(BaseOxmlElement):
    """
    17.16.9 ddList (Drop-Down List Form Field Properties)

    <xsd:complexType name="CT_FFDDList">
        <xsd:sequence>
            <xsd:element name="result" type="CT_DecimalNumber" minOccurs="0"/>
            <xsd:element name="default" type="CT_DecimalNumber" minOccurs="0"/>
            <xsd:element name="listEntry" type="CT_String" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
    </xsd:complexType>

    """
    default = ZeroOrOne("w:default")
    result = ZeroOrOne("w:result")
    listEntry = OneOrMore("w:listEntry")

# ------------------------------
# Check Box
# ------------------------------

class CT_FFCheckBox(BaseOxmlElement): # noqa
    """
    17.16.7 checkBox (Checkbox Form Field Properties)

    <xsd:complexType name="CT_FFCheckBox">
        <xsd:sequence>
        <xsd:choice>
            <xsd:element name="size" type="CT_HpsMeasure"/>
            <xsd:element name="sizeAuto" type="CT_OnOff"/>
        </xsd:choice>
        <xsd:element name="default" type="CT_OnOff" minOccurs="0"/>
        <xsd:element name="checked" type="CT_OnOff" minOccurs="0"/>
        </xsd:sequence>
    </xsd:complexType>
    """

    checked = OneAndOnlyOne('w:checked')
    default = ZeroOrOne('w:default')
    # NOTE: ignoring size and sizeAuto for now


# ------------------------------
# Text Input
# ------------------------------

class CT_FFTextInput(BaseOxmlElement): # noqa
    """
    17.16.33 textInput (Text Box Form Field Properties)

    <xsd:complexType name="CT_FFTextInput">
        <xsd:sequence>
            <xsd:element name="type" type="CT_FFTextType" minOccurs="0"/>
            <xsd:element name="default" type="CT_String" minOccurs="0"/>
            <xsd:element name="maxLength" type="CT_DecimalNumber" minOccurs="0"/>
            <xsd:element name="format" type="CT_String" minOccurs="0"/>
        </xsd:sequence>
    </xsd:complexType>
    """

    type_ = ZeroOrOne('w:type')
    default = ZeroOrOne('w:default')
    format_ = ZeroOrOne('w:format')



class ST_FFTextType(XsdStringEnumeration):
    """
    Valid values for <w:fldChar fldCharType=""> attribute

    <xsd:simpleType name="ST_FFTextType">
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="regular"/>
            <xsd:enumeration value="number"/>
            <xsd:enumeration value="date"/>
            <xsd:enumeration value="currentTime"/>
            <xsd:enumeration value="currentDate"/>
            <xsd:enumeration value="calculated"/>
        </xsd:restriction>
    </xsd:simpleType>
    """

    REGULAR = "regular"
    NUMBER = "number"
    DATE = "date"
    CURRENTTIME = "currentTime"
    CURRENTDATE = "currentDate"
    CALCULATED = "calculated"

    _members = (REGULAR, NUMBER, DATE, CURRENTTIME, CURRENTDATE, CALCULATED)


class CT_FFTextType(BaseOxmlElement): # noqa
    """
    Used for ``<w:pStyle>`` and ``<w:tblStyle>`` elements and others,
    containing a style name in its ``val`` attribute.
    """
    val = RequiredAttribute('w:val', ST_FFTextType)

#--     @classmethod
#--     def new(cls, nsptagname, val):
#--         """
#--         Return a new ``CT_String`` element with tagname *nsptagname* and
#--         ``val`` attribute set to *val*.
#--         """
#--         elm = OxmlElement(nsptagname)
#--         elm.val = val
#--         return elm


