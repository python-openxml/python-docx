
python-docx
===========

Release v\ |version| (:ref:`Installation <install>`)

*python-docx* is a Python library for creating and updating Microsoft Word
(.docx) files.


What it can do
--------------

.. |img| image:: /_static/img/example-docx-01.png

Here's an example of what |docx| can do:

============================================  ===============================================================
|img|                                         ::

                                                from docx import Document
                                                from docx.shared import Inches

                                                document = Document()

                                                document.add_heading('Document Title', 0)

                                                p = document.add_paragraph('A plain paragraph having some ')
                                                p.add_run('bold').bold = True
                                                p.add_run(' and some ')
                                                p.add_run('italic.').italic = True

                                                document.add_heading('Heading, level 1', level=1)
                                                document.add_paragraph('Intense quote', style='IntenseQuote')

                                                document.add_paragraph(
                                                    'first item in unordered list', style='ListBullet'
                                                )
                                                document.add_paragraph(
                                                    'first item in ordered list', style='ListNumber'
                                                )

                                                document.add_picture('monty-truth.png', width=Inches(1.25))

                                                table = document.add_table(rows=1, cols=3)
                                                hdr_cells = table.rows[0].cells
                                                hdr_cells[0].text = 'Qty'
                                                hdr_cells[1].text = 'Id'
                                                hdr_cells[2].text = 'Desc'
                                                for item in recordset:
                                                    row_cells = table.add_row().cells
                                                    row_cells[0].text = str(item.qty)
                                                    row_cells[1].text = str(item.id)
                                                    row_cells[2].text = item.desc

                                                document.add_page_break()

                                                document.save('demo.docx')
============================================  ===============================================================

|docx| is also capable of modifying existing documents:

::

  import docx

  # open the document template
  document = docx.Document('Document.docx')

  # get a list of all inline_shapes of the document
  shapes = document.inline_shapes

  # print the number of paragraphs
  print('The document has {} inline_shapes.'.format(len(shapes)))

  # the document has no inline_shapes, create one with its attributes:
  # height, type, width

  # get the "metadata" of the document
  properties = document.core_properties

  # modify the attributes of the "metadata"
  # author, category, comments, content_status, created, identifier, keywords,
  # language, last_modified_by, last_printed, modified, revision, subject,
  # title, version

  # get a list of all paragraphs
  paragraphs = document.paragraphs

  # print the number of paragraphs
  print('The document has {} paragraphs(s).'.format(len(paragraphs)))

  # get the parapgraph of choice by list index (here: 9 paragraph)
  paragraph_of_choice = paragraphs[3]

  # modify the paragraph with its attributes:
  # add_run(), alignment, clear(), insert_paragraph_before(), paragraph_format,
  # runs, style, text

  # e.g. print the text of the paragraph
  print(paragraph_of_choice.text)

  # get a list of all sections 
  sections = document.sections

  # print the number of sections
  print('The document has {} sections(s).'.format(len(sections)))

  # get the section of choice by list index (here: only 1 section)
  section_of_choice = sections[0]

  # modify the attributes of the section:
  # bottom_margin, footer_distance, gutter, header_distance, left_margin,
  # orientation, page_height, page_width, right_margin, start_type, top_margin

  # get tables
  tables = document.tables

  # print the number of tables
  print('The document has {} table(s).'.format(len(tables)))

  # get the table of choice by list index (here: only 1 table)
  table_of_choice = tables[0]

  # modify table which has the following attributes/methods():
  # add_column(), add_row(), alignment, autofit, cell, column_cells, columns,
  # row_cells, rows, style, table_direction

  # e.g. add cell text
  table_of_choice.cell(row_idx=2, col_idx=2).text = 'hello'
  table_of_choice.cell(row_idx=2, col_idx=3).text = 'world'

  # save the modified document (override the existing copied file)
  document.save('./Document_copy.docx')

The document before (left) and after (right) the modification:

.. |img_before| image:: /_static/img/example-docx-before-modification.png
.. |img_after| image:: /_static/img/example-docx-after-modification.png

============================================  ============================================
|img_before|                                  |img_after|
============================================  ============================================

User Guide
----------

.. toctree::
   :maxdepth: 1

   user/install
   user/quickstart
   user/documents
   user/text
   user/sections
   user/api-concepts
   user/styles-understanding
   user/styles-using
   user/shapes


API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   api/document
   api/style
   api/text
   api/table
   api/section
   api/shape
   api/dml
   api/shared
   api/enum/index


Contributor Guide
-----------------

.. toctree::
   :maxdepth: 1

   dev/analysis/index
