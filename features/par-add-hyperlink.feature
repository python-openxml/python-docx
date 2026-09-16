Feature: Append an external hyperlink to a paragraph
  In order to link document text to external resources
  As a developer using python-docx
  I need to create a hyperlink on the paragraph's owning story part

  Scenario Outline: Create a hyperlink in a story
    Given a hyperlink authoring paragraph in a <story>
     When I append an external hyperlink between ordinary runs
     Then the new hyperlink and surrounding text survive saving

    Examples:
      | story  |
      | body   |
      | cell   |
      | header |
      | footer |

  Scenario Outline: Preserve the supplied destination
    Given a hyperlink authoring paragraph in a body
     When I append a hyperlink to <address>
     Then the supplied hyperlink destination survives saving unchanged

    Examples:
      | address                                            |
      | https://example.com/a%20b?q=one&lang=en#intro         |
      | mailto:hello@example.com?subject=Hello%20there       |
      | ../guide with spaces.docx                           |
      | custom:resource                                    |

  Scenario: Populate an empty hyperlink
    Given a hyperlink authoring paragraph in a body
     When I create a hyperlink without an initial label
     Then I can build its label by appending runs

  Scenario: Reject an empty address without changing the document
    Given a hyperlink authoring paragraph in a body
     When I try to create a hyperlink with an empty address
     Then no hyperlink or relationship has been added

  Scenario Outline: Supply a tooltip when creating a hyperlink
    Given a hyperlink authoring paragraph in a body
     When I create a hyperlink with a <value> tooltip
     Then the assigned tooltip survives saving

    Examples:
      | value     |
      | populated |
      | empty     |
      | absent    |

  Scenario: Reject an invalid creation tooltip without changing the document
    Given a hyperlink authoring paragraph in a body
     When I try to create a hyperlink with invalid XML in its tooltip
     Then no hyperlink or relationship has been added
