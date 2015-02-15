Feature: Access document collections
  In order to operate on objects related to a document
  As a developer using python-docx
  I need a way to access each of the document's collections


  Scenario: Access the inline shapes collection of a document
     Given a document having inline shapes
      Then I can access the inline shape collection of the document


  Scenario: Access the paragraphs in the document body as a list
     Given a document containing three paragraphs
      Then document.paragraphs is a list containing three paragraphs
