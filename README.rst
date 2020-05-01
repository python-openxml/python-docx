Bayoo-docx
===========

Python library forked from  `python-docx <github.com/python-openxml/python-docx/>`_.

The main purpose of the fork was to add implementation for comments and footnotes to the library

Installation
------------

Use the package manager `pip <pypi.org/project/bayoo-docx/>`_ to install bayoo-docx.


`pip install bayoo-docx`

Usage
-----
::
    
    import docx
    
    document = docx.Document()

    paragraph = document.add_paragraph('text') # create new paragraph

    comment = paragraph.add_comment('comment',author='Obay Daba',initials= 'od') # create a comment'

    paragraph.add_footnote('footnote text') # add a footnote



License
--------------

`MIT <https://choosealicense.com/licenses/mit/>`_