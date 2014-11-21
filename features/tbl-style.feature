Feature: Query and apply a table style
  In order to maintain consistent formatting of tables
  As a developer using python-docx
  I need the ability to query and apply a table style

  Scenario: Access table style
     Given a table having an applied style
      Then I can get the table style name

  Scenario: Apply table style
     Given a table
      When I apply a style to the table
      Then the table style matches the name I applied
