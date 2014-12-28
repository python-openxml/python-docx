Feature: Access style font
  In order to discover or change the character formatting of a style
  As a developer using python-docx
  I need access to the font of a style


  Scenario Outline: Get style font
    Given a style of type <style-type>
     Then style.font is the Font object for the style

    Examples: Style types
      | style-type              |
      | WD_STYLE_TYPE.CHARACTER |
      | WD_STYLE_TYPE.PARAGRAPH |
      | WD_STYLE_TYPE.TABLE     |
