Feature: Append an inline picture on its own paragraph
  In order add an image to a document
  As a programmer using the basic python-docx API
  I need a method that adds a picture in its own paragraph

  Scenario: Add a picture at native size
    Given a document
     When I add a picture specifying only the image file
     Then the document contains the inline picture
      And the picture has its native width and height

  Scenario: Add a picture specifying both width and height
    Given a document
     When I add a picture specifying 1.75" width and 2.5" height
     Then the picture width is 1.75 inches
      And the picture height is 2.5 inches

  Scenario: Add a picture specifying only width
    Given a document
     When I add a picture specifying a width of 1.5 inches
     Then the picture height is 2.14 inches

  Scenario: Add a picture specifying only height
    Given a document
     When I add a picture specifying a height of 1.5 inches
     Then the picture width is 1.05 inches
