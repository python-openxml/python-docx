Feature: Split paragraph on rendered page-breaks
  In order to extract document content with high page-attribution fidelity
  As a developer using python-docx
  I need to a way to split a paragraph on its first rendered page break


  Scenario: RenderedPageBreak.preceding_paragraph_fragment is the content before break
    Given a rendered_page_break in a paragraph
     Then rendered_page_break.preceding_paragraph_fragment is the content before break


  Scenario: RenderedPageBreak.preceding_paragraph_fragment includes the hyperlink
    Given a rendered_page_break in a hyperlink
     Then rendered_page_break.preceding_paragraph_fragment includes the hyperlink


  Scenario: RenderedPageBreak.following_paragraph_fragment is the content after break
    Given a rendered_page_break in a paragraph
     Then rendered_page_break.following_paragraph_fragment is the content after break


  Scenario: RenderedPageBreak.following_paragraph_fragment excludes the hyperlink
    Given a rendered_page_break in a hyperlink
     Then rendered_page_break.following_paragraph_fragment excludes the hyperlink
