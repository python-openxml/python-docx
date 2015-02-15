Feature: Access document sections
  In order to operate on an individual section
  As a developer using python-docx
  I need access to each section in the section collection


  Scenario: Access section in section collection
     Given a section collection containing 3 sections
      Then len(sections) is 3
       And I can iterate over the sections
       And I can access a section by index
