.. :changelog:


#Release History BayooG/bayoo-docx forked from (python-openxmm/python-docx)


0.2.8 (2020-05-02)

- add comments implementation on a run level
- fix issue with comments date (comments dates are set to current date)


0.2.4 (2019-9-4)

- loop over all the document chieldern (Paragraphs, Tables, Sections) with the right order `document.elements`
- addons to Paragraph Object (delete, heading_level, merge_paragraph )
- Add low-level implementation for comments part
- Add oxml element for <w:comments> element and sub-elements
- Add add_comment() method for docx.text.Paragraph 
- Add low-level implementation for footnotes part
- Add oxml element for <w:footnotes> element and sub-elements
- Add add_footnote() method for docx.text.Paragraph 


