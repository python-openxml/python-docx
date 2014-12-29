Feature: Access run font
  In order to discover or change the character formatting of a run
  As a developer using python-docx
  I need access to the font of a run


  Scenario: Access the font of a run
    Given a run
     Then run.font is the Font object for the run
