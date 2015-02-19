Feature: Get and set font color
  In order to work with the color of text
  As a developer using python-docx
  I need a way to get and set the text color


  Scenario Outline: Get font color type
    Given a font having <type> color
     Then font.color.type is <value>

    Examples: Color type settings
      | type    | value |
      | no      | None  |
      | auto    | AUTO  |
      | an RGB  | RGB   |
      | a theme | THEME |


  Scenario Outline: Get font RGB color
    Given a font having <type> color
     Then font.color.rgb is <value>

    Examples: Color type settings
      | type    | value  |
      | no      | None   |
      | auto    | None   |
      | an RGB  | 008000 |
      | a theme | 4f81bd |


  Scenario Outline: Set font RGB color
    Given a font having <type> color
     When I assign <value> to font.color.rgb
     Then font.color.type is <type-value>
     Then font.color.rgb is <rgb-value>

    Examples: Color type settings
      | type    | value  | type-value | rgb-value |
      | no      | f00ba5 | RGB        | f00ba5    |
      | auto    | 2468ac | RGB        | 2468ac    |
      | an RGB  | feeb1e | RGB        | feeb1e    |
      | a theme | 987bac | RGB        | 987bac    |
      | an RGB  | None   | None       | None      |
      | a theme | None   | None       | None      |
