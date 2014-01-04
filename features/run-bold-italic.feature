Feature: Apply bold or italic to run
  In order to apply emphasis to a particular word or phrase in a paragraph
  As a python-docx developer
  I need a way to query and set bold and italic on a run

  Scenario: Apply bold to a run
    Given a run
     When I assign True to its bold property
     Then the run appears in bold typeface

  Scenario: Remove bold from a run
    Given a run having bold set on
     When I assign None to its bold property
     Then the run appears with its inherited bold setting

  Scenario: Set bold off unconditionally
    Given a run
     When I assign False to its bold property
     Then the run appears without bold regardless of its style hierarchy
