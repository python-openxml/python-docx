Feature: Get and set style properties
  In order to adjust styles to suit my needs
  As a developer using python-docx
  I need a set of read/write style properties


  Scenario: Get style id
    Given a style having a known style id
     Then style.style_id is the known style id


  Scenario: Set style id
    Given a style having a known style id
     When I assign a new value to style.style_id
     Then style.style_id is the new style id
