Feature: Read and write inline shape alternative text
  In order to describe a picture without changing its appearance
  As a python-docx developer
  I need public access to the placed shape's description and title

  Scenario: Save a description and title
    Given a picture with no alternative text
     When I set its description and title
      And I save and reopen the picture document
     Then its description and title are preserved

  Scenario: Preserve an empty description and remove a title
    Given a picture with no alternative text
     When I set its description and title
      And I empty its description and remove its title
      And I save and reopen the picture document
     Then its description is empty and its title is absent
