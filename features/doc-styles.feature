Feature: Access a document style
  In order to operate on a particular document style
  As a developer using python-docx
  I access to each style in the document style collection


  Scenario Outline: Access style in style collection
    Given a document having <styles-state>
     Then len(styles) is <style-count>
      And I can iterate over its styles
      And I can access a style by style id
      And I can access a style by its UI name

    Examples: having styles or not
      | styles-state   | style-count |
      | a styles part  |      6      |
      | no styles part |      4      |
