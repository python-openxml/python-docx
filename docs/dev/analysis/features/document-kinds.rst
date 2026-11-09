
Macro-enabled documents and templates
=====================================

Besides the regular document (``.docx``), Word saves three other kinds of
WordprocessingML package: the macro-enabled document (``.docm``), the template
(``.dotx``) and the macro-enabled template (``.dotm``).

All four share the same package structure and the same main document part XML
(``word/document.xml`` with a ``<w:document>`` root element). The only thing
that tells Word which kind of file it is opening is the content-type of the main
document part, declared in ``[Content_Types].xml``. The file extension must
match it; Word refuses to open a file whose extension disagrees with that
content-type.

Macro-enabled packages additionally contain a VBA project part, a binary (OLE
compound file) ``word/vbaProject.bin`` related to the main document part, and
usually a ``word/vbaData.xml`` part related to it. These are opaque to
|docx|: they are loaded as generic parts and written back unchanged.

See issues #212, #284 and #363.


Candidate protocol
------------------

.. highlight:: python

::

  >>> document = Document('macros.docm')
  >>> document.part.content_type
  'application/vnd.ms-word.document.macroEnabled.main+xml'
  >>> document.save('macros-edited.docm')  # -- still a .docm, macros preserved --

  >>> document = Document('letterhead.dotx')
  >>> document.part.content_type
  'application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml'


Word behavior
-------------

* Word opens each kind with the matching extension. A template opened by
  double-click creates a new document based on it; opened with *File > Open*,
  the template itself is edited.
* Renaming a ``.dotx`` file to ``.docx`` (or the reverse) without changing the
  content-type produces a file Word reports as corrupt.
* Saving a ``.docm`` as ``.docx`` in Word drops the VBA project parts and
  changes the content-type.


Content types
-------------

========= ======================================================================================
Extension Main document part content-type
========= ======================================================================================
.docx     application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml
.docm     application/vnd.ms-word.document.macroEnabled.main+xml
.dotx     application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml
.dotm     application/vnd.ms-word.template.macroEnabledTemplate.main+xml
========= ======================================================================================

These are available as ``docx.opc.constants.CONTENT_TYPE`` members
``WML_DOCUMENT_MAIN``, ``WML_DOCUMENT_MACRO_MAIN``, ``WML_TEMPLATE_MAIN`` and
``WML_TEMPLATE_MACRO_MAIN``.


Specimen XML
------------

.. highlight:: xml

``[Content_Types].xml`` of a ``.docm`` package (abbreviated)::

  <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="bin" ContentType="application/vnd.ms-office.vbaProject"/>
    <Default Extension="rels"
             ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/word/document.xml"
              ContentType="application/vnd.ms-word.document.macroEnabled.main+xml"/>
    ...
  </Types>

``word/_rels/document.xml.rels`` relationship to the VBA project::

  <Relationship Id="rId1"
                Type="http://schemas.microsoft.com/office/2006/relationships/vbaProject"
                Target="vbaProject.bin"/>


Out of scope
------------

* Reading, adding or changing macros (the VBA project is a binary format).
* Converting a package from one kind to another (e.g. a template to a
  document).
