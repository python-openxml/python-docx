Feature: Access TabStop objects
  In order to interact with an individual tab stop for a paragraph or style
  As a developer using python-docx
  I need methods to create, access, and remove a tab stop


  Scenario Outline: TabStops.__len__
    Given a tab_stops having <count> tab stops
     Then len(tab_stops) is <count>

    Examples: tab_stop counts
      | count |
      |   0   |
      |   3   |


  @wip
  Scenario: Access an existing TabStop object
    Given a tab_stops having 3 tab stops
     Then I can iterate the TabStops object
      And I can access a tab stop by index
