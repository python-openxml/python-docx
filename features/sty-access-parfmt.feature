Feature: Access style paragraph format
  In order to discover or change the paragraph formatting of a style
  As a developer using python-docx
  I need access to the paragraph format of a style


  Scenario Outline: Get style paragraph format
    Given a style of type <style-type>
     Then style.paragraph_format is the ParagraphFormat object for the style

    Examples: Style types
      | style-type              |
      | WD_STYLE_TYPE.PARAGRAPH |
      | WD_STYLE_TYPE.TABLE     |
