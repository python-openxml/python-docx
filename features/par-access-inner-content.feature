Feature: Access paragraph inner-content including hyperlinks
  In order to extract paragraph content with high-fidelity
  As a developer using python-docx
  I need to access differentiated paragraph content in document order


  Scenario Outline: Paragraph.contains_page_break reports presence of page-break
    Given a paragraph having <zero-or-more> rendered page breaks
     Then paragraph.contains_page_break is <value>

    Examples: Paragraph.contains_page_break cases
      | zero-or-more | value |
      | no           | False |
      | one          | True  |
      | two          | True  |


  Scenario Outline: Paragraph.hyperlinks contains Hyperlink for each link in paragraph
    Given a paragraph having <zero-or-more> hyperlinks
     Then paragraph.hyperlinks has length <value>
      And paragraph.hyperlinks contains only Hyperlink instances

    Examples: Paragraph.hyperlinks cases
      | zero-or-more | value |
      | no           |   0   |
      | one          |   1   |
      | three        |   3   |


  Scenario: Paragraph.iter_inner_content() generates the paragraph's runs and hyperlinks
    Given a paragraph having three hyperlinks
     Then paragraph.iter_inner_content() generates the paragraph runs and hyperlinks


  Scenario Outline: Paragraph.rendered_page_breaks contains paragraph RenderedPageBreaks
    Given a paragraph having <zero-or-more> rendered page breaks
     Then paragraph.rendered_page_breaks has length <value>
      And paragraph.rendered_page_breaks contains only RenderedPageBreak instances

    Examples: Paragraph.rendered_page_breaks cases
      | zero-or-more | value |
      | no           |   0   |
      | one          |   1   |
      | two          |   2   |


  Scenario: Paragraph.text contains both run-text and hyperlink-text
    Given a paragraph having three hyperlinks
     Then paragraph.text contains the text of both the runs and the hyperlinks
