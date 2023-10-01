Feature: Access run inner-content including rendered page-breaks
  In order to extract run content with high-fidelity
  As a developer using python-docx
  I need to access differentiated run content in document order


  Scenario Outline: Run.contains_page_break reports presence of page-break
    Given a run having <zero-or-more> rendered page breaks
     Then run.contains_page_break is <value>

    Examples: Run.contains_page_break cases
      | zero-or-more | value |
      | no           | False |
      | one          | True  |
      | two          | True  |


  Scenario: Run.iter_inner_content() generates the run's text and rendered page-breaks
    Given a run having two rendered page breaks
     Then run.iter_inner_content() generates the run text and rendered page-breaks


  Scenario: Run.text contains the text content of the run
    Given a run having mixed text content
     Then run.text contains the text content of the run
