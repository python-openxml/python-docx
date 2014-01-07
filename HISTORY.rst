.. :changelog:

Release History
---------------

0.3.0a4 (2014-01-07)
++++++++++++++++++++++

- Complete Python 3 support, tested on Python 3.3

0.3.0a3 (2014-01-06)
++++++++++++++++++++++

- Fix setup.py error on some Windows installs

0.3.0a1 (2014-01-05)
++++++++++++++++++++++

- Full object-oriented rewrite
- Feature-parity with prior version
- text: add paragraph, run, text, bold, italic
- table: add table, add row, add column
- styles: specify style for paragraph, table
- picture: add inline picture, auto-scaling
- breaks: add page break
- tests: full pytest and behave-based 2-layer test suite

0.3.0dev1 (2013-12-14)
++++++++++++++++++++++

- Round-trip .docx file, preserving all parts and relationships
- Load default "template" .docx on open with no filename
- Open from stream and save to stream (file-like object)
- Add paragraph at and of document
