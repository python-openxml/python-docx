
python-docx
===========

Release v\ |version| (:ref:`Installation <install>`)

.. include:: ../README.rst


Status
------

|docx| is very usable, but still in pre-release status. We are very interested
in alpha users who can provide real-life use cases with which to exercise the
API. The code is thoroughly tested, so finding bugs is not our purpose. We
believe tests should do that job, not users. However, API changes become
painful after release, so we'd like to get it as right as we can before that.
A post-alpha release is expected within a few weeks, say Feb 1, 2014.


What it can do
--------------

Here's an example of what |docx| can do:

.. figure:: /_static/img/example-docx-01.png

|

::

    from docx import Document

    document = Document()

    document.add_heading('Document Title', 0)
    document.add_paragraph('A plain paragraph.')
    document.add_heading('Heading, level 1', level=1)
    document.add_paragraph('Intense quote', style='IntenseQuote')
    document.add_bullet('first item in unordered list')
    document.add_list_item('first item in ordered list')

    document.add_picture('monty-truth.png')

    table = document.add_table(rows=1, cols=3)
    table.style = 'LightShading-Accent1'
    header_cells = table.rows[0].cells
    header_cells[0].text = 'Qty'
    header_cells[1].text = 'Id'
    header_cells[2].text = 'Desc'
    for item in recordset:
        row_cells = table.add_row().cells
        row_cells[0].text = str(item.qty)
        row_cells[1].text = str(item.id)
        row_cells[2].text = item.desc
    
    document.add_page_break()

    document.save('demo.docx')


User Guide
----------

.. toctree::
   :maxdepth: 1

   user/install
   user/documents
   user/api-concepts
   user/styles
   user/tables
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
