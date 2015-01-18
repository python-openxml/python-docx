Feature: Get and set style properties
  In order to adjust a style to suit my needs
  As a developer using python-docx
  I need a set of read/write style properties


  Scenario: Get style id
    Given a style having a known style id
     Then style.style_id is the known style id


  Scenario: Set style id
    Given a style having a known style id
     When I assign a new style id to the style
     Then style.style_id is the new style id


  Scenario: Get style type
    Given a style having a known type
     Then style.type is the known type


  Scenario: Get name
    Given a style having a known name
     Then style.name is the known name


  Scenario: Set name
    Given a style having a known name
     When I assign a new name to the style
     Then style.name is the new name


  Scenario Outline: Get base style
    Given a style based on <base-style>
     Then style.base_style is <value>

    Examples: Base style values
      | base-style | value            |
      | no style   | None             |
      | Normal     | styles['Normal'] |


  Scenario Outline: Set base style
    Given a style based on <base-style>
     When I assign <assigned-value> to style.base_style
     Then style.base_style is <value>

    Examples: Base style values
      | base-style | assigned-value   | value            |
      | no style   | styles['Normal'] | styles['Normal'] |
      | Normal     | styles['Base']   | styles['Base']   |
      | Base       | None             | None             |


  @wip
  Scenario Outline: Get hidden value
    Given a style having hidden set <setting>
     Then style.hidden is <value>

    Examples: Style hidden values
      | setting    | value |
      | on         | True  |
      | off        | False |
      | no setting | False |


  @wip
  Scenario Outline: Set hidden value
    Given a style having hidden set <setting>
     When I assign <new-value> to style.hidden
     Then style.hidden is <value>

    Examples: Style hidden values
      | setting    | new-value | value |
      | no setting | True      | True  |
      | on         | False     | False |
