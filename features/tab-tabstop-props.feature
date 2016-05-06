Feature: Tab stop properties
  To change the properties of an individual tab stop
  As a developer using python-docx
  I need a set of read/write properties on TabStop


  @wip
  Scenario Outline: Get TabStop.position
    Given a tab stop 0.5 inches <in-or-out> from the paragraph left edge
     Then tab_stop.position is <position>

    Examples: tab stop positions
      | in-or-out | position |
      |    in     |  457200  |
      |    out    | -457200  |


  @wip
  Scenario Outline: Get TabStop.alignment
    Given a tab stop having <alignment> alignment
     Then tab_stop.alignment is <alignment>

    Examples: tab stop alignments
      | alignment |
      | LEFT      |
      | RIGHT     |


  @wip
  Scenario Outline: Get TabStop.leader
    Given a tab stop having <leader> leader
     Then tab_stop.leader is <value>

    Examples: tab stop leaders
      | leader       | value  |
      | no specified | SPACES |
      | a dotted     | DOTS   |
