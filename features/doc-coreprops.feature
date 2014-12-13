Feature: Read and write core document properties
  In order to find documents and make them manageable by digital means
  As a developer using python-docx
  I need to access and modify the Dublin Core metadata for a document

  @wip
  Scenario: read the core properties of a document
     Given a document having known core properties
      Then I can access the core properties object
       And the core property values match the known values
