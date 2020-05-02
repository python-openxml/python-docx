Bayoo-docx
==========

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

    paragraph1 = document.add_paragraph('text') # create new paragraph

    comment = paragraph.add_comment('comment',author='Obay Daba',initials= 'od') # add a comment on the entire paragraph

    paragraph2 = document.add_paragraph('text') # create another paragraph

    run = paragraph2.add_run('texty') add a run to the paragraph

    run.add_comment('comment') # add a comment only for the run text 

    paragraph.add_footnote('footnote text') # add a footnote



License
-------

`MIT <https://choosealicense.com/licenses/mit/>`_
