Feature: Query and apply a table style
  In order to maintain consistent formatting of tables
  As a developer using python-docx
  I need the ability to get and set the style of a table


  Scenario Outline: Get the style of a table
    Given a table having <style> style
     Then table.style is styles['<value>']

    Examples: Table styles
      | style                    | value                  |
      | no explicit              | Normal Table           |
      | Table Grid               | Table Grid             |
      | Light Shading - Accent 1 | Light Shading Accent 1 |


  Scenario Outline: Apply a table style
    Given a table having <style> style
     When I assign <value> to table.style
     Then table.style is styles['<style-name>']

    Examples: Character style transitions
      | style       | value                  | style-name   |
      | no explicit | Table Grid             | Table Grid   |
      | no explicit | styles['Table Grid']   | Table Grid   |
      | Table Grid  | Normal Table           | Normal Table |
      | Table Grid  | styles['Normal Table'] | Normal Table |
      | Table Grid  | None                   | Normal Table |
