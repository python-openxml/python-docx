Feature: Access document collections
  In order to operate on objects related to a document
  As a developer using python-docx
  I need a way to access each of the document's collections


  Scenario: Access the inline shapes collection of a document
     Given a document having inline shapes
      Then I can access the inline shape collection of the document
