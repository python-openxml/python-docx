Feature: Access document sections
  In order to discover and apply section-level settings
  As a developer using python-docx
  I need a way to access document sections


  Scenario: Access section collection of a document
     Given a document having three sections
      Then I can access the section collection of the document
       And the length of the section collection is 3


  Scenario: Access section in section collection
     Given a section collection
      Then I can iterate over the sections
       And I can access a section by index
