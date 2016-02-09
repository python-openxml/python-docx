@wip
Feature: Get or set font hightlight color
  In order to customize the character highlight color of text in a document
  As a python-docx developer
  I need a set of read/write the highlight_color property on the Font object

  @wip
  Scenario Outline: Get highlight color
    Given a font having highlight color <highlight_color>
     Then font.highlight_color is <value>

    Examples: font.highlight_color values
      | highlight_color | value       |
      | None            | None        |
      | Yellow          | YELLOW      |
      | Bright Green    | BRIGHTGREEN |
      | Turquoise       | TURQUOISE   |
      | Pink            | PINK        |
      | Blue            | BLUE        |
      | Red             | RED         |
      | Dark Blue       | DARKBLUE    |
      | Teal            | TEAL        |
      | Green           | GREEN       |
      | Violet          | VIOLET      |
      | Dark Red        | DARKRED     |
      | Dark Yellow     | DARKYELLOW  |
      | Dark Gray       | GRAY50      |
      | Light Gray      | GRAY25      |
      | Black           | BLACK       |

  @wip
  Scenario Outline: Get highlight color
    Given a font having highlight color <highlight_color>
     Then the XML value is <xml_value>

    Examples: font.highlight_color values
      | highlight_color | xml_value   |
      | Yellow          | yellow      |
      | Bright Green    | green       |
      | Turquoise       | cyan        |
      | Pink            | magenta     |
      | Blue            | blue        |
      | Red             | red         |
      | Dark Blue       | darkBlue    |
      | Teal            | darkCyan    |
      | Green           | darkGreen   |
      | Violet          | darkMagenta |
      | Dark Red        | darkRed     |
      | Dark Yellow     | darkYellow  |
      | Dark Gray       | darkGray    |
      | Light Gray      | lightGray   |
      | Black           | black       |

  @wip
  Scenario Outline: Set highlight color
    Given a font having highlight color <highlight_color>
     When I assign <value> to font.highlight_color
     Then font.highlight_color is <value>

    Examples: font.highlight_color values
      | highlight_color | value       |
      | None            | YELLOW      |
      | Yellow          | None        |
      | Bright Green    | BRIGHTGREEN |
      | Turquoise       | GREEN       |
      | Black           | BLUE        |
      | Black           | BLACK       |
      
      