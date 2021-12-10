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


  Scenario: Access an existing TabStop object
    Given a tab_stops having 3 tab stops
     Then I can iterate the TabStops object
      And I can access a tab stop by index


  Scenario Outline: TabStops.add_tab_stop()
    Given a tab_stops having <count> tab stops
     When I add a tab stop
     Then len(tab_stops) is <new-count>
      And the tab stops are sequenced in position order

    Examples: tab stop object counts
      | count | new-count |
      |   0   |     1     |
      |   3   |     4     |


  Scenario: TabStops.__delitem__()
    Given a tab_stops having 3 tab stops
     When I remove a tab stop
     Then len(tab_stops) is 2
      And the removed tab stop is no longer present in tab_stops


  Scenario: TabStops.clear_all()
    Given a tab_stops having 3 tab stops
     When I call tab_stops.clear_all()
     Then len(tab_stops) is 0
