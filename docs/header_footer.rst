Headers and Footers Api Summary
===========================

The following methods are added to the main_document_part (aka docx.document.Document)

.. code-block:: python
    class Document(ElementProxy):
        def clear_headers(self):
            """ clears all headers from a docx
            """

        def add_header(self):
            """ removes all existing headers from a docx then adds a new footer
            :returns: a new Header instance
            """

        def clear_footers(self):
            """ clears all footers from a docx
            """

        def add_footer(self):
            """ removes all existing footers from a docx then adds a new footer
            :returns: a new Footer instance
            """


.. code-block:: python
    class Header(BlockItemContainer):
        """ Proxy object wrapping around a CT_Hdr <w:hdr> element

        paragraph = header.add_paragraph()
        run_text = paragraph.add_run('foobar', style='FOO')
        run_img = paragraph.add_run()
        run_img.add_picture(logo, width, height)
        """


.. code-block:: python
    class Footer(BlockItemContainer):
        """ Proxy object wrapping around a CT_Ftr <w:ftr> element

        paragraph = footer.add_paragraph()
        run_text = paragraph.add_run('foobar', style='FOO')
        run_img = paragraph.add_run()
        run_img.add_picture(logo, width, height)
        """



What currently works:

Clear Headers / Footers.
Add Header / Footer.
Add Header / Footer paragraph with style.
Add Header / Footer paragraph run with style.
Add Header / Footer paragraph run with image.
Add Header / Footer paragraph run with other inline shapes (probably).

What might not work so hot:

Editing existing headers easily.

What does not work:

Adding a second header to a document that already has a header.
(The `document.add_header` method clears all headers first.)
But this sounds like an edge case. Maybe it's not needed.
