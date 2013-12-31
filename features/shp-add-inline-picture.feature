Feature: Add inline picture
  In order to generate a document containing an image
  As a python-docx developer
  I need the ability to add an inline picture to a document

  Scenario: Add inline picture to document
    Given a document
     When I add an inline picture to the document
     Then its inline shape type is WD_INLINE_SHAPE.PICTURE
      And the document contains the inline picture

  Scenario: Add inline picture from stream
    Given a document
     When I add an inline picture from a file-like object
     Then its inline shape type is WD_INLINE_SHAPE.PICTURE
      And the document contains the inline picture
