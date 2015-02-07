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


  Scenario: Get latent style name
    Given a latent style having a known name
     Then latent_style.name is the known name


  Scenario Outline: Get latent style display sort order
    Given a latent style having priority of <setting>
     Then latent_style.priority is <value>

    Examples: latent_style.priority values
      | setting    | value |
      | no setting | None  |
      | 42         | 42    |


  Scenario Outline: Set latent style display sort order
    Given a latent style having priority of <setting>
     When I assign <new-value> to latent_style.priority
     Then latent_style.priority is <value>

    Examples: Latent style priority values
      | setting    | new-value | value |
      | no setting | 42        | 42    |
      | 42         | 24        | 24    |
      | 42         | None      | None  |


  Scenario Outline: Get on/off latent style properties
    Given a latent style having <prop-name> set <setting>
     Then latent_style.<prop-name> is <value>

    Examples: Latent style hidden values
      | prop-name        | setting    | value |
      | hidden           | on         | True  |
      | hidden           | off        | False |
      | hidden           | no setting | None  |
      | locked           | on         | True  |
      | locked           | off        | False |
      | locked           | no setting | None  |
      | quick_style      | on         | True  |
      | quick_style      | off        | False |
      | quick_style      | no setting | None  |
      | unhide_when_used | on         | True  |
      | unhide_when_used | off        | False |
      | unhide_when_used | no setting | None  |


  Scenario Outline: Set on/off latent style properties
    Given a latent style having <prop-name> set <setting>
     When I assign <new-value> to latent_style.<prop-name>
     Then latent_style.<prop-name> is <value>

    Examples: Latent style hidden values
      | prop-name        | setting    | new-value | value |
      | hidden           | no setting | True      | True  |
      | hidden           | on         | False     | False |
      | hidden           | off        | None      | None  |
      | locked           | no setting | False     | False |
      | locked           | off        | True      | True  |
      | locked           | on         | None      | None  |
      | quick_style      | no setting | True      | True  |
      | quick_style      | on         | False     | False |
      | quick_style      | off        | None      | None  |
      | unhide_when_used | no setting | False     | False |
      | unhide_when_used | off        | True      | True  |
      | unhide_when_used | on         | False     | False |
