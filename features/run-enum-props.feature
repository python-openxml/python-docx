Feature: Query or apply enumerated run property
  In order to query or change an enumerated font property of a word or phrase
  As a python-docx developer
  I need a way to query and set the enumerated properties on a run


  @wip
  Scenario Outline: Get underline value of a run
    Given a run having <underline-type> underline
     Then the run underline property value is <underline-value>

    Examples: underline property values
      | underline-type | underline-value     |
      | inherited      | None                |
      | no             | False               |
      | single         | True                |
      | double         | WD_UNDERLINE.DOUBLE |
