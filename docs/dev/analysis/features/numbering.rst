
Numbering Part
==============

... having to do with numbering sequences for ordered lists, etc. ...


Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_Numbering">
    <xsd:sequence>
      <xsd:element name="numPicBullet"      type="CT_NumPicBullet"  minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="abstractNum"       type="CT_AbstractNum"   minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="num"               type="CT_Num"           minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="numIdMacAtCleanup" type="CT_DecimalNumber" minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_Num">
    <xsd:sequence>
      <xsd:element name="abstractNumId" type="CT_DecimalNumber"/>
      <xsd:element name="lvlOverride"   type="CT_NumLvl"        minOccurs="0" maxOccurs="9"/>
    </xsd:sequence>
    <xsd:attribute name="numId" type="ST_DecimalNumber" use="required"/>
  </xsd:complexType>

  <xsd:complexType name="CT_NumLvl">
    <xsd:sequence>
      <xsd:element name="startOverride" type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="lvl"           type="CT_Lvl"           minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute name="ilvl" type="ST_DecimalNumber" use="required"/>
  </xsd:complexType>

  <xsd:complexType name="CT_NumPr">
    <xsd:sequence>
      <xsd:element name="ilvl"            type="CT_DecimalNumber"        minOccurs="0"/>
      <xsd:element name="numId"           type="CT_DecimalNumber"        minOccurs="0"/>
      <xsd:element name="numberingChange" type="CT_TrackChangeNumbering" minOccurs="0"/>
      <xsd:element name="ins"             type="CT_TrackChange"          minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_DecimalNumber">
    <xsd:attribute name="val" type="ST_DecimalNumber" use="required"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_DecimalNumber">
    <xsd:restriction base="xsd:integer"/>
  </xsd:simpleType>
