Feature: Each run has a read/write style
  In order to use the stylesheet capability built into Word
  As a developer using python-docx
  I need the ability to get and set the character style of a run


  Scenario Outline: Get the character style of a run
    Given a run having <style> style
     Then run.style is styles['<value>']

    Examples: Character styles
      | style       | value                  |
      | no explicit | Default Paragraph Font |
      | Emphasis    | Emphasis               |
      | Strong      | Strong                 |


  Scenario Outline: Set the style of a run
    Given a run having <style> style
     When I assign <value> to run.style
     Then run.style is styles['<style-name>']

    Examples: Character style transitions
      | style       | value              | style-name             |
      | no explicit | Emphasis           | Emphasis               |
      | no explicit | styles['Emphasis'] | Emphasis               |
      | Emphasis    | Strong             | Strong                 |
      | Emphasis    | styles['Strong']   | Strong                 |
      | Strong      | None               | Default Paragraph Font |
