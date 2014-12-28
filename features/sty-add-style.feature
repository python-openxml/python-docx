Feature: Add a style
  In order to customize the available styles in a document
  As a developer using python-docx
  I need a way to add a new style


  Scenario Outline: Add a style
    Given a document having known styles
     When I call add_style('<name>', <type>, builtin=<builtin>)
     Then the document has one additional style
      And styles['<name>'] is a style
      And style.type is <type>
      And style.builtin is <builtin>

    Examples: New style varieties
      | name        | type                    | builtin |
      | Heading 1   | WD_STYLE_TYPE.PARAGRAPH | True    |
      | Inline Code | WD_STYLE_TYPE.CHARACTER | False   |
      | List Bullet | WD_STYLE_TYPE.LIST      | True    |
      | Shipments   | WD_STYLE_TYPE.TABLE     | False   |
