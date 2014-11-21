Feature: Get and set table properties
  In order to format a table to my requirements
  As a developer using python-docx
  I need a way to get and set a table's properties


  Scenario Outline: Get autofit layout setting
    Given a table having an autofit layout of <autofit-setting>
     Then the reported autofit setting is <reported-autofit>

    Examples: table autofit settings
      | autofit-setting     | reported-autofit |
      | no explicit setting | autofit          |
      | autofit             | autofit          |
      | fixed               | fixed            |


  Scenario Outline: Set autofit layout setting
    Given a table having an autofit layout of <autofit-setting>
     When I set the table autofit to <new-setting>
     Then the reported autofit setting is <reported-autofit>

    Examples: table column width values
      | autofit-setting     | new-setting | reported-autofit |
      | no explicit setting | autofit     | autofit          |
      | no explicit setting | fixed       | fixed            |
      | fixed               | autofit     | autofit          |
      | autofit             | autofit     | autofit          |
      | fixed               | fixed       | fixed            |
      | autofit             | fixed       | fixed            |
