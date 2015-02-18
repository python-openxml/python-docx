Feature: Get and set font color
  In order to work with the color of text
  As a developer using python-docx
  I need a way to get and set the text color


  @wip
  Scenario Outline: Get font color type
    Given a font having <type> color
     Then font.color.type is <value>

    Examples: Color type settings
      | type    | value |
      | no      | None  |
      | auto    | AUTO  |
      | an RGB  | RGB   |
      | a theme | THEME |
