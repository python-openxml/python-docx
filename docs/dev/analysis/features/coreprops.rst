
Core Document Properties
========================

The Open XML format provides for a set of descriptive properties to be
maintained with each document. One of these is the *core file properties*.
The core properties are common to all Open XML formats and appear in
document, presentation, and spreadsheet files. The 'Core' in core document
properties refers to `Dublin Core`_, a metadata standard that defines a core
set of elements to describe resources.

The core properties are described in Part 2 of the ISO/IEC 29500 spec, in
Section 11. The names of some core properties in |docx| are changed from
those in the spec to conform to the MS API.

Other properties such as company name are custom properties, held in
``app.xml``.


Candidate Protocol
------------------

::

    >>> document = Document()
    >>> core_properties = document.core_properties
    >>> core_properties.author
    'python-docx'
    >>> core_properties.author = 'Brian'
    >>> core_properties.author
    'Brian'


Properties
----------

15 properties are supported. All unicode values are limited to 255 characters
(not bytes).

author *(unicode)*
    Note: named 'creator' in spec. An entity primarily responsible for making
    the content of the resource. (Dublin Core)

category *(unicode)*
    A categorization of the content of this package. Example values for this
    property might include: Resume, Letter, Financial Forecast, Proposal,
    Technical Presentation, and so on. (Open Packaging Conventions)

comments *(unicode)*
    Note: named 'description' in spec. An explanation of the content of the
    resource. Values might include an abstract, table of contents, reference
    to a graphical representation of content, and a free-text account of the
    content. (Dublin Core)

content_status *(unicode)*
    The status of the content. Values might include “Draft”, “Reviewed”, and
    “Final”. (Open Packaging Conventions)

created *(datetime)*
    Date of creation of the resource. (Dublin Core)

identifier *(unicode)*
    An unambiguous reference to the resource within a given context.
    (Dublin Core)

keywords *(unicode)*
    A delimited set of keywords to support searching and indexing. This is
    typically a list of terms that are not available elsewhere in the
    properties. (Open Packaging Conventions)

language *(unicode)*
    The language of the intellectual content of the resource. (Dublin Core)

last_modified_by *(unicode)*
    The user who performed the last modification. The identification is
    environment-specific. Examples include a name, email address, or employee
    ID. It is recommended that this value be as concise as possible.
    (Open Packaging Conventions)

last_printed *(datetime)*
    The date and time of the last printing. (Open Packaging Conventions)

modified *(datetime)*
    Date on which the resource was changed. (Dublin Core)

revision *(int)*
    The revision number. This value might indicate the number of saves or
    revisions, provided the application updates it after each revision.
    (Open Packaging Conventions)

subject *(unicode)*
    The topic of the content of the resource. (Dublin Core)

title *(unicode)*
    The name given to the resource. (Dublin Core)

version *(unicode)*
    The version designator. This value is set by the user or by the
    application. (Open Packaging Conventions)


Specimen XML
------------

.. highlight:: xml

core.xml produced by Microsoft Word::

    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <cp:coreProperties
        xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/"
        xmlns:dcmitype="http://purl.org/dc/dcmitype/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <dc:title>Core Document Properties Exploration</dc:title>
      <dc:subject>PowerPoint core document properties</dc:subject>
      <dc:creator>Steve Canny</dc:creator>
      <cp:keywords>powerpoint; open xml; dublin core; microsoft office</cp:keywords>
      <dc:description>
        One thing I'd like to discover is just how line wrapping is handled
        in the comments. This paragraph is all on a single
        line._x000d__x000d_This is a second paragraph separated from the
        first by two line feeds.
      </dc:description>
      <cp:lastModifiedBy>Steve Canny</cp:lastModifiedBy>
      <cp:revision>2</cp:revision>
      <dcterms:created xsi:type="dcterms:W3CDTF">2013-04-06T06:03:36Z</dcterms:created>
      <dcterms:modified xsi:type="dcterms:W3CDTF">2013-06-15T06:09:18Z</dcterms:modified>
      <cp:category>analysis</cp:category>
    </cp:coreProperties>


Schema Excerpt
--------------

::

    <xs:schema
      targetNamespace="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
      xmlns="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
      xmlns:xs="http://www.w3.org/2001/XMLSchema"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:dcterms="http://purl.org/dc/terms/"
      elementFormDefault="qualified"
      blockDefault="#all">

      <xs:import
        namespace="http://purl.org/dc/elements/1.1/"
        schemaLocation="http://dublincore.org/schemas/xmls/qdc/2003/04/02/dc.xsd"/>
      <xs:import
        namespace="http://purl.org/dc/terms/"
        schemaLocation="http://dublincore.org/schemas/xmls/qdc/2003/04/02/dcterms.xsd"/>
      <xs:import
        id="xml"
        namespace="http://www.w3.org/XML/1998/namespace"/>

      <xs:element name="coreProperties" type="CT_CoreProperties"/>

      <xs:complexType name="CT_CoreProperties">
        <xs:all>
          <xs:element name="category"        type="xs:string"   minOccurs="0"/>
          <xs:element name="contentStatus"   type="xs:string"   minOccurs="0"/>
          <xs:element ref="dcterms:created"                     minOccurs="0"/>
          <xs:element ref="dc:creator"                          minOccurs="0"/>
          <xs:element ref="dc:description"                      minOccurs="0"/>
          <xs:element ref="dc:identifier"                       minOccurs="0"/>
          <xs:element name="keywords"        type="CT_Keywords" minOccurs="0"/>
          <xs:element ref="dc:language"                         minOccurs="0"/>
          <xs:element name="lastModifiedBy"  type="xs:string"   minOccurs="0"/>
          <xs:element name="lastPrinted"     type="xs:dateTime" minOccurs="0"/>
          <xs:element ref="dcterms:modified"                    minOccurs="0"/>
          <xs:element name="revision"        type="xs:string"   minOccurs="0"/>
          <xs:element ref="dc:subject"                          minOccurs="0"/>
          <xs:element ref="dc:title"                            minOccurs="0"/>
          <xs:element name="version"         type="xs:string"   minOccurs="0"/>
        </xs:all>
      </xs:complexType>

      <xs:complexType name="CT_Keywords" mixed="true">
        <xs:sequence>
          <xs:element name="value" minOccurs="0" maxOccurs="unbounded" type="CT_Keyword"/>
        </xs:sequence>
        <xs:attribute ref="xml:lang" use="optional"/>
      </xs:complexType>

      <xs:complexType name="CT_Keyword">
        <xs:simpleContent>
          <xs:extension base="xs:string">
            <xs:attribute ref="xml:lang" use="optional"/>
          </xs:extension>
        </xs:simpleContent>
      </xs:complexType>

    </xs:schema>


.. _Dublin Core:
   http://en.wikipedia.org/wiki/Dublin_Core
