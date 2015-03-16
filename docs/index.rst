
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
   api/settings
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
