
Character Style
===============

Word allows a set of run-level properties to be given a name. The set of
properties is called a *character style*. All the settings may be applied to
a run in a single action by setting the style of the run.

Example:

   The normal font of a document is 10 point Times Roman. From time to time,
   a Python class name appears in-line in the text. These short runs of
   Python text are to appear in 9 point Courier. A character style named "Code"
   is defined such that these words or phrases can be set to the distinctive
   font and size in a single step.

   Later, it is decided that 10 point Menlo should be used for inline code
   instead. The "Code" character style is updated to the new settings and all
   instances of inline code in the document immediately appear in the new
   font.


Protocol
--------

There are two call protocols related to character style: getting and setting
the character style of a run, and specifying a style when creating a run.

Getting and setting the style of a run::

    >>> run = p.add_run()
    >>> run.style
    None
    >>> run.style = 'Emphasis'
    >>> run.style
    'Emphasis'
    >>> run.style = None
    >>> run.style
    None

Assigning |None| to ``Run.style`` causes any applied character style to be
removed. A run without a character style inherits the character style of its
containing paragraph.

Specifying the style of a run on creation::

    >>> run = p.add_run()
    >>> run.style
    None
    >>> run = p.add_run(style='Emphasis')
    >>> run.style
    'Emphasis'
    >>> run = p.add_run('text in this run', 'Strong')
    >>> run.style
    'Strong'



Specimen XML
------------

.. highlight:: xml

A baseline regular run::

  <w:p>
    <w:r>
      <w:t>This is a regular paragraph.</w:t>
    </w:r>
  </w:p>

Adding *Emphasis* character style::

  <w:p>
    <w:r>
      <w:rPr>
        <w:rStyle w:val="Emphasis"/>
      </w:rPr>
      <w:t>This paragraph appears in Emphasis character style.</w:t>
    </w:r>
  </w:p>

A style that appears in the Word user interface (UI) with one or more spaces
in its name, such as "Subtle Emphasis", will generally have a style ID with
those spaces removed. In this example, "Subtle Emphasis" becomes
"SubtleEmphasis"::

  <w:p>
    <w:r>
      <w:rPr>
        <w:rStyle w:val="SubtleEmphasis"/>
      </w:rPr>
      <w:t>a few words in Subtle Emphasis style</w:t>
    </w:r>
  </w:p>



Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_R">  <!-- flattened for readibility -->
    <xsd:sequence>
      <xsd:element name="rPr" type="CT_RPr" minOccurs="0"/>
      <xsd:group   ref="EG_RunInnerContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="rsidRPr" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidDel" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidR"   type="ST_LongHexNumber"/>
  </xsd:complexType>

  <xsd:complexType name="CT_RPr">  <!-- flattened for readibility -->
    <xsd:sequence>
      <xsd:group   ref="EG_RPrBase" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="rPrChange" type="CT_RPrChange" minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:group name="EG_RPrBase">
    <xsd:choice>
      <xsd:element name="rStyle"          type="CT_String"/>
      <xsd:element name="rFonts"          type="CT_Fonts"/>
      <xsd:element name="b"               type="CT_OnOff"/>
      <!-- 36 others -->
    </xsd:choice>
  </xsd:group>

  <xsd:complexType name="CT_String">
    <xsd:attribute name="val" type="s:ST_String" use="required"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_String">
    <xsd:restriction base="xsd:string"/>
  </xsd:simpleType>
