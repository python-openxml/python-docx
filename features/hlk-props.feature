Feature: Access hyperlink properties
  In order to access the URL and other details for a hyperlink
  As a developer using python-docx
  I need properties on Hyperlink


  Scenario: Hyperlink.address has the URL of the hyperlink
    Given a hyperlink
     Then hyperlink.address is the URL of the hyperlink


  Scenario Outline: Hyperlink.contains_page_break reports presence of page-break
    Given a hyperlink having <zero-or-more> rendered page breaks
     Then hyperlink.contains_page_break is <value>

    Examples: Hyperlink.contains_page_break cases
      | zero-or-more | value |
      | no           | False |
      | one          | True  |


  Scenario: Hyperlink.fragment has the URI fragment of the hyperlink
    Given a hyperlink having a URI fragment
     Then hyperlink.fragment is the URI fragment of the hyperlink


  Scenario Outline: Hyperlink.runs contains Run for each run in hyperlink
    Given a hyperlink having <zero-or-more> runs
     Then hyperlink.runs has length <value>
      And hyperlink.runs contains only Run instances

    Examples: Hyperlink.runs cases
      | zero-or-more | value |
      | one          |   1   |
      | two          |   2   |


  Scenario: Hyperlink.text has the visible text of the hyperlink
    Given a hyperlink
     Then hyperlink.text is the visible text of the hyperlink


  Scenario Outline: Hyperlink.url is the full URL of an internet hyperlink
    Given a hyperlink having address <address> and fragment <fragment>
     Then hyperlink.url is <url>

    Examples: Hyperlink.url cases
      | address                   | fragment       | url                       |
      | ''                        | linkedBookmark | ''                        |
      | https://foo.com           | ''             | https://foo.com           |
      | https://foo.com?q=bar     | ''             | https://foo.com?q=bar     |
      | http://foo.com/           | intro          | http://foo.com/#intro     |
      | https://foo.com?q=bar#baz | ''             | https://foo.com?q=bar#baz |
      | court-exif.jpg            | ''             | court-exif.jpg            |
