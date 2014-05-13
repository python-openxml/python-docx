
python-docx
===========

Release v\ |version| (:ref:`Installation <install>`)

.. include:: ../README.rst


What it can do
--------------

.. |img| image:: /_static/img/example-docx-01.png

Here's an example of what |docx| can do:

======  ======================================================================
|img|   ::

          from docx import Document

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
          recordset = [
              {'qty': 1, 'id': 101, 'desc': 'Spam'},
              {'qty': 2, 'id': 42, 'desc': 'Eggs'},
              {'qty': 3, 'id': 631, 'desc': 'Spam, spam, eggs, and spam'},
          ]
          for item in recordset:
              row_cells = table.add_row().cells
              row_cells[0].text = str(item['qty'])
              row_cells[1].text = str(item['id'])
              row_cells[2].text = item['desc']

          document.add_page_break()

          document.save('demo.docx')
======  ======================================================================


User Guide
----------

.. toctree::
   :maxdepth: 1

   user/install
   user/quickstart
   user/documents
   user/api-concepts
   user/styles
   user/shapes
   user/text


API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   api/document
   api/table
   api/text
   api/shape
   api/shared


Contributor Guide
-----------------

.. toctree::
   :maxdepth: 1

   dev/analysis/index
