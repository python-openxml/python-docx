Feature: Access document collections
  In order to operate on objects related to a document
  As a developer using python-docx
  I need a way to access each of the document's collections


  Scenario: Access the inline shapes collection of a document
     Given a document having inline shapes
      Then document.inline_shapes is an InlineShapes object


  Scenario: Access the paragraphs in the document body as a list
     Given a document containing three paragraphs
      Then document.paragraphs is a list containing three paragraphs


  Scenario: Access the section collection of a document
     Given a document having sections
      Then document.sections is a Sections object


  Scenario: Access the styles collection of a document
    Given a document having styles
     Then document.styles is a Styles object


  Scenario: Access the tables collection of a document
    Given a document having three tables
     Then document.tables is a list containing three tables
