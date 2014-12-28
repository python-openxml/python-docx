Feature: Get and set style properties
  In order to adjust a style to suit my needs
  As a developer using python-docx
  I need a set of read/write style properties


  Scenario: Get name
    Given a style having a known name
     Then style.name is the known name


  Scenario: Set name
    Given a style having a known name
     When I assign a new name to the style
     Then style.name is the new name


  Scenario: Get style id
    Given a style having a known style id
     Then style.style_id is the known style id


  Scenario: Set style id
    Given a style having a known style id
     When I assign a new value to style.style_id
     Then style.style_id is the new style id


  Scenario: Get style type
    Given a style having a known type
     Then style.type is the known type
