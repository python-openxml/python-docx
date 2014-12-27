Feature: Each paragraph has a read/write style
  In order to use the stylesheet capability built into Word
  As a developer using python-docx
  I need the ability to get and set the style of a paragraph


  Scenario Outline: Get the style of a paragraph
     Given a paragraph having <style> style
      Then paragraph.style is <expected-value>

    Examples: ways of specifying a style
      | style        | expected-value |
      | no specified | Normal         |
      | a missing    | Normal         |
      | Heading 1    | Heading 1      |
      | Body Text    | Body Text      |


  Scenario Outline: Set the style of a paragraph
     Given a paragraph
      When I assign a <style-spec> to paragraph.style
      Then the paragraph has the style I set

    Examples: ways of specifying a style
      | style-spec   |
      | style object |
      | style name   |
