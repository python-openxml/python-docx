Feature: Get and set style properties
  In order to adjust styles to suit my needs
  As a developer using python-docx
  I need a set of read/write style properties


  @wip
  Scenario: Get style id
    Given a style having a known style id
     Then style.style_id is the known style id


  @wip
  Scenario: Set style id
    Given a style having a known style id
     When I assign a new style id to the style
     Then style.style_id is the new style id
