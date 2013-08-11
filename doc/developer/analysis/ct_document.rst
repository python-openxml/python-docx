###############
``CT_Document``
###############

.. highlight:: xml

.. csv-table::
   :header-rows: 0
   :stub-columns: 1
   :widths: 15, 50

   Schema Name  , CT_Document
   Spec Name    , Document
   Tag(s)       , w:document
   Namespace    , wordprocessingml (wml.xsd)
   Spec Section , 17.2.3


Analysis
========


attributes
^^^^^^^^^^

===========  ===  ===================
name          #   type
===========  ===  ===================
conformance   ?   ST_ConformanceClass
===========  ===  ===================


child elements
^^^^^^^^^^^^^^

==========  ===  =============
name         #   type
==========  ===  =============
background   ?   CT_Background
body         ?   CT_Body
==========  ===  =============


Spec text
^^^^^^^^^

    This element specifies the contents of a main document part in
    a WordprocessingML document.

    Consider the basic structure of the main document part in a basic
    WordprocessingML document, as follows::

        <w:document>
          <w:body>
            <w:p/>
          </w:body>
        </w:document>

    All of the contents of the main document part are contained beneath the
    document element.


Schema excerpt
^^^^^^^^^^^^^^

::

  <xsd:complexType name="CT_Document">
    <xsd:sequence>
      <xsd:element name="background" type="CT_Background" minOccurs="0"/>
      <xsd:element name="body"       type="CT_Body"       minOccurs="0" maxOccurs="1"/>
    </xsd:sequence>
    <xsd:attribute name="conformance" type="s:ST_ConformanceClass"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Background">
    <xsd:sequence>
      <xsd:sequence maxOccurs="unbounded">
        <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:vml" minOccurs="0" maxOccurs="unbounded"/>
        <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:office:office" minOccurs="0" maxOccurs="unbounded"/>
      </xsd:sequence>
      <xsd:element name="drawing" type="CT_Drawing" minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute name="color"      type="ST_HexColor"       use="optional"/>
    <xsd:attribute name="themeColor" type="ST_ThemeColor"     use="optional"/>
    <xsd:attribute name="themeTint"  type="ST_UcharHexNumber" use="optional"/>
    <xsd:attribute name="themeShade" type="ST_UcharHexNumber" use="optional"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Body">
    <xsd:sequence>
      <xsd:group ref="EG_BlockLevelElts" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="sectPr" minOccurs="0" maxOccurs="1" type="CT_SectPr"/>
    </xsd:sequence>
  </xsd:complexType>
