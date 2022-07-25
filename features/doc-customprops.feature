Feature: Read and write custom document properties
  In order to find documents and make them manageable by digital means
  As a developer using python-docx
  I need to access and modify the Dublin Core metadata for a document


  Scenario: read the custom properties of a document
     Given a document having known custom properties
      Then I can access the custom properties object
       And the custom property values match the known values


  Scenario: change the custom properties of a document
     Given a document having known custom properties
      When I assign new values to the custom properties
      Then the custom property values match the new values


  Scenario: a default custom properties part is added if doc doesn't have one
     Given a document having no custom properties part
      When I access the custom properties object
      Then a custom properties part with no values is added


  Scenario: set custom properties on a document that doesn't have one
     Given a document having no custom properties part
      When I assign new values to the custom properties
      Then the custom property values match the new values
