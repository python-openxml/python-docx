Feature: Tab stop properties
  To change the properties of an individual tab stop
  As a developer using python-docx
  I need a set of read/write properties on TabStop


  Scenario Outline: Get tab stop position
    Given a tab stop 0.5 inches <in-or-out> from the paragraph left edge
     Then tab_stop.position is <position>

    Examples: tab stop positions
      | in-or-out | position |
      |    in     |  457200  |
      |    out    | -457200  |


  Scenario Outline: Set tab stop position
    Given a tab stop 0.5 inches in from the paragraph left edge
     When I assign <value> to tab_stop.position
      Then tab_stops at position 1 is <value>

    Examples: tab stop positions
      |  value  |
      |  228600 |
      | -228600 |
      
      
  Scenario Outline: Maintain tab stop position order when changing position
    Given a tab_stops having 3 tab stops
      When I change the tab at <index> position to <value>
        Then the tab stops are sequenced in position order
        
      Examples: tab stop positions
      | index | value   |
      | 0     | 2285000 |
      | 2     | 1371600 | 

  Scenario Outline: Get tab stop alignment
    Given a tab stop having <alignment> alignment
     Then tab_stop.alignment is <alignment>

    Examples: tab stop alignments
      | alignment |
      | LEFT      |
      | RIGHT     |


  Scenario Outline: Set tab stop alignment
   Given a tab stop having <alignment> alignment
    When I assign <member> to tab_stop.alignment
     Then tab_stop.alignment is <member>

    Examples: tab stop alignments
      | alignment | member |
      | LEFT      | CENTER |
      | RIGHT     | LEFT   |


  Scenario Outline: Get tab stop leader
    Given a tab stop having <leader> leader
     Then tab_stop.leader is <value>

    Examples: tab stop leaders
      | leader       | value  |
      | no specified | SPACES |
      | a dotted     | DOTS   |


  Scenario Outline: Set tab stop leader
   Given a tab stop having <leader> leader
    When I assign <member> to tab_stop.leader
     Then tab_stop.leader is <member>

    Examples: tab stop leaders
      | leader       | member |
      | no specified | DOTS   |
      | a dotted     | SPACES |
