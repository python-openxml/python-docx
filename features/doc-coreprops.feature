Feature: Read and write core document properties
  In order to find documents and make them manageable by digital means
  As a developer using python-docx
  I need to access and modify the Dublin Core metadata for a document


  Scenario: read the core properties of a document
     Given a document having known core properties
      Then I can access the core properties object
       And the core property values match the known values


  Scenario: change the core properties of a document
     Given a document having known core properties
      When I assign new values to the properties
      Then the core property values match the new values


  Scenario: a default core properties part is added if doc doesn't have one
     Given a document having no core properties part
      When I access the core properties object
      Then a core properties part with default values is added
