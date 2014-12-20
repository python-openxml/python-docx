Feature: Access document styles
  In order to discover and manipulate document styles
  As a developer using python-docx
  I need a way to access document styles


  Scenario Outline: Access document styles collection
    Given a document having <styles-state>
     Then I can access the document styles collection
      And len(styles) is <style-count>

    Examples: having styles or not
      | styles-state   | style-count |
      | a styles part  |      6      |
      | no styles part |      4      |


  Scenario: Access style in style collection
    Given a document having a styles part
     Then I can iterate over its styles
      And I can access a style by style id
      And I can access a style by its UI name
