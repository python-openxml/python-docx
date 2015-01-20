Feature: Get and set latent style properties
  In order to adjust latent style properties to suit my needs
  As a developer using python-docx
  I need a set of read/write latent style properties


  Scenario Outline: Get default latent style properties
    Given a latent styles object with known defaults
     Then latent_styles.<prop-name> is <value>

    Examples: known latent_styles property values
      | prop-name                   | value |
      | default_priority            | 99    |
      | load_count                  | 276   |
      | default_to_hidden           | True  |
      | default_to_locked           | False |
      | default_to_quick_style      | False |
      | default_to_unhide_when_used | True  |


  Scenario Outline: Set default latent style properties
    Given a latent styles object with known defaults
     When I assign <new-value> to latent_styles.<prop-name>
     Then latent_styles.<prop-name> is <value>

    Examples: known latent_styles property values
      | prop-name                   | new-value | value |
      | default_priority            |   42      | 42    |
      | load_count                  |   240     | 240   |
      | default_to_hidden           |   False   | False |
      | default_to_locked           |   True    | True  |
      | default_to_quick_style      |   True    | True  |
      | default_to_unhide_when_used |   False   | False |
