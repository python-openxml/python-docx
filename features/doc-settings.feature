Feature: Access to document settings
  In order to operate on document-level settings
  As a developer using python-docx
  I access to settings stored in the settings part


  Scenario Outline: Access document settings
    Given a document having <a-or-no> settings part
     Then document.settings is a Settings object

    Examples: having a settings part or not
      | a-or-no   |
      | a         |
      | no        |
