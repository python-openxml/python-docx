Feature: Tab stop properties
  To change the properties of an individual tab stop
  As a developer using python-docx
  I need a set of read/write properties on TabStop


  Scenario Outline: Get TabStop.position
    Given a tab stop 0.5 inches <in-or-out> from the paragraph left edge
     Then tab_stop.position is <position>

    Examples: tab stop positions
      | in-or-out | position |
      |    in     |  457200  |
      |    out    | -457200  |


  Scenario Outline: Set TabStop.position
    Given a tab stop 0.5 inches in from the paragraph left edge
     When I assign <value> to tab_stop.position
      Then tab_stop.position is <value>
       And the tab stops are sequenced in position order

    Examples: tab stop positions
      |  value  |
      |  228600 |
      | -914400 |


  Scenario Outline: Get TabStop.alignment
    Given a tab stop having <alignment> alignment
     Then tab_stop.alignment is <alignment>

    Examples: tab stop alignments
      | alignment |
      | LEFT      |
      | RIGHT     |


  Scenario Outline: Set TabStop.alignment
   Given a tab stop having <alignment> alignment
    When I assign <member> to tab_stop.alignment
     Then tab_stop.alignment is <member>

    Examples: tab stop alignments
      | alignment | member |
      | LEFT      | CENTER |
      | RIGHT     | LEFT   |


  Scenario Outline: Get TabStop.leader
    Given a tab stop having <leader> leader
     Then tab_stop.leader is <value>

    Examples: tab stop leaders
      | leader       | value  |
      | no specified | SPACES |
      | a dotted     | DOTS   |


  Scenario Outline: Set TabStop.leader
   Given a tab stop having <leader> leader
    When I assign <member> to tab_stop.leader
     Then tab_stop.leader is <member>

    Examples: tab stop leaders
      | leader       | member |
      | no specified | DOTS   |
      | a dotted     | SPACES |
