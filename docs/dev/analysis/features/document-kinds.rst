
Macro-enabled documents and templates
=====================================

Besides the regular document (``.docx``), Word saves three other kinds of
WordprocessingML package: the macro-enabled document (``.docm``), the template
(``.dotx``) and the macro-enabled template (``.dotm``).

Up to v1.2.0, |docx| refuses to open them, raising ``ValueError: file '...' is not
a Word file, content type is '...'`` (issues #212, #284, #363). This page
describes how the four kinds differ, how macros are stored, the experiments
showing that macros survive a load/save cycle unchanged, and the limits of the
approach.


Candidate protocol
------------------

.. highlight:: python

::

  >>> document = Document('macros.docm')
  >>> document.part.content_type
  'application/vnd.ms-word.document.macroEnabled.main+xml'
  >>> document.add_paragraph('Added by python-docx')
  >>> document.save('macros-edited.docm')  # -- still a .docm, macros preserved --

  >>> document = Document('letterhead.dotx')
  >>> document.part.content_type
  'application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml'

No new API is added. ``docx.Document()`` accepts the three additional kinds and
the package keeps its kind when saved.


How the four kinds differ
-------------------------

All four share the same package structure and the same main document part XML
(``word/document.xml`` with a ``<w:document>`` root element, same schema). The
only thing that tells Word which kind of file it is opening is the content-type
of the main document part, declared in ``[Content_Types].xml``:

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

The file extension must agree with that content-type; Word refuses to open a
file whose extension does not match ("the file format or file extension is not
valid").


How macros are stored
---------------------

A macro-enabled package (``.docm`` or ``.dotm``) adds these parts to the regular
document structure:

``word/vbaProject.bin``
  The VBA project: an OLE compound file (MS-OVBA) holding the compressed source
  and compiled p-code of every module, the project references and, when
  password-protected, the protection data. Content-type
  ``application/vnd.ms-office.vbaProject``, related from the main document part
  with relationship type
  ``http://schemas.microsoft.com/office/2006/relationships/vbaProject``.

``word/vbaData.xml``
  Word-specific macro metadata (``<wne:vbaSuppData>``: one ``<wne:mcd>`` per
  macro, with its name and encryption flag). Content-type
  ``application/vnd.ms-word.vbaData+xml``, related from ``vbaProject.bin``
  (``word/_rels/vbaProject.bin.rels``) with relationship type
  ``http://schemas.microsoft.com/office/2006/relationships/wordVbaData``.

Optionally, depending on what the author did in Word:

* ``word/vbaProjectSignature.bin`` (and agile/V3 variants) – digital signature of
  the VBA project, related from ``vbaProject.bin``.
* ``word/customizations.xml`` – keyboard shortcuts assigned to macros
  (``keyMapCustomizations`` relationship from the main document part).
* ``word/activeX/*`` – ActiveX controls and their binary persistence parts.

|docx| has no part class for any of these. On load, the OPC layer instantiates
them as generic |Part| objects (via ``PartFactory.default_part_type``), keeping
the original blob and relationships; on save they are written back with the
same partname, content-type and relationships, byte for byte. This is the same
mechanism that already preserves any part |docx| does not understand in a
``.docx`` file (footnotes, glossary document, custom XML, etc.).


Implementation
--------------

The change is limited to recognising the three additional main-document
content-types:

* ``docx.opc.constants.CONTENT_TYPE``: add the three content-types.
* ``docx/__init__.py``: map each of them to |DocumentPart| in
  ``PartFactory.part_type_for``, so the main document part gets the same proxy
  as in a ``.docx`` file.
* ``docx.api.Document()``: accept any of the four main-document content-types
  instead of only ``WML_DOCUMENT_MAIN``.

The content-type of the main document part is stored on the part when loaded
and written back unchanged on save, which is what keeps the package kind.


Experiments
-----------

The following was used to establish that macros are preserved. The scripts
mentioned are not part of the library.

1. **Source files made by Word.** A document exercising most |docx| features
   (headings, styles, runs and fonts, paragraph formatting, tables including
   merged and nested cells, pictures in five formats, comments, four sections
   with headers/footers) was saved by Word (Office 16, Windows) as
   ``.docm``, ``.dotx`` and ``.dotm``, after adding a VBA module to the
   ``.docm``/``.dotm``. The module contains a ``PythonDocxCheck`` macro that
   reports document statistics and whether the last paragraph is the one added
   by |docx|, plus a marker constant ``PYDOCX-MACRO-PROBE v1``.

2. **Without the change (python-docx 1.2.0 from PyPI).** The ``.docx`` opens;
   the ``.docm``, ``.dotx`` and ``.dotm`` all raise ``ValueError: ... is not a
   Word file``.

3. **Load, edit, save with the change.** Each file was opened with
   ``docx.Document()``, a paragraph was appended, and it was saved under a new
   name with the same extension. Comparing the source and result packages:

   * main document part content-type unchanged (``.docm`` stays ``.docm``, etc.),
   * same set of parts: none lost, none added,
   * every binary part byte-identical: ``word/vbaProject.bin`` and all five
     images,
   * ``vbaProject.bin`` still related from the main document part, and
     ``vbaData.xml`` from ``vbaProject.bin``,
   * VBA source extracted from the saved ``vbaProject.bin`` (``oletools``)
     still contains both macros and the marker.

4. **Heavier edits.** The same files were edited further (paragraph inserted
   at the top, table cell text replaced, comment added, core properties
   changed) and saved. Same results as in 3.

5. **Back in Word.** The saved ``.docm``/``.dotm`` files open in Word without a
   repair prompt, the edits are shown, and after enabling content
   ``PythonDocxCheck`` runs and detects the paragraph added by |docx|.

The acceptance tests ``features/api-open-document.feature`` reproduce 2–3 in an
automated way with small fixtures: ``doc-default.docm``/``.dotx``/``.dotm`` are
``doc-default.docx`` with the main document content-type changed and, for the
macro-enabled ones, the VBA parts of the Word-made file above (a real VBA
project containing ``PythonDocxCheck``) added. The scenarios check the package
kind and that ``vbaProject.bin`` is preserved byte for byte.


Limits and unintended consequences
----------------------------------

* **Macros are opaque.** They cannot be read, added, changed or removed through
  the |docx| API; they are carried along unchanged.

* **No conversion between kinds.** A template stays a template, a ``.docm``
  stays a ``.docm``. Saving under another extension (e.g. a ``.dotx`` package
  as ``foo.docx``) produces a file Word refuses to open; |docx| does not check
  the extension against the content-type, as before. Converting would need a
  new API (out of scope; see #363 for the workaround of setting the private
  ``DocumentPart._content_type``).

* **Digital signatures.** A signed VBA project stays signed and valid, because
  ``vbaProject.bin`` and the signature parts are not modified. Document-level
  (XAdES package) signatures are invalidated by any save, as for ``.docx``.

* **Parts must be reachable by relationship.** As for ``.docx``, |docx| only
  loads parts reachable from the package relationships. Word always relates the
  VBA parts as described above; a hand-made package with an unrelated
  ``vbaProject.bin`` would lose it on save. This is unchanged behaviour.

* **Default template.** ``docx.Document()`` with no argument still creates a
  ``.docx``. Creating a macro-enabled file or template from scratch is out of
  scope.

* **Templates opened as documents.** |docx| edits the template itself, as Word
  does with *File > Open*. It does not create a new document based on the
  template, which is what Word does when a template is double-clicked.

* **Other OOXML packages.** Opening a ``.xlsx``/``.pptx`` (or any package whose
  main part is not one of the four content-types) still raises ``ValueError``.
