    # Bayoo-docx

    Python library forked from  [python-docx](https://github.com/python-openxml/python-docx/).

    ## Installation

    Use the package manager [pip](https://pypi.org/project/bayoo-docx/) to install bayoo-docx.

    ```bash
    pip install bayoo-docx
    ```

    ## Features
    
    The main purpose of forking [python-docx](https://github.com/python-openxml/python-docx/) was to add comments and footnotes implementation
    - low-level support for comments & footnotes (on oxml level)

    ## Usage

    ```python
    import docx

    document = docx.Document()
    paragraph = document.add_paragraph('text') # create new paragraph
    comment = paragraph.add_comment('comment',author='Obay Daba',initials= 'od') # create a comment'
    paragraph.add_footnote('footnote text') # add a footnote
    ```


    ## License
    [MIT](https://choosealicense.com/licenses/mit/)