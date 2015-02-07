Feature: Add or delete a latent style
  In order to determine which latent styles are defined in a document
  As a developer using python-docx
  I need a way to add and delete a latent style


  Scenario: Add a latent style
    Given a document having known styles
     When I add a latent style named 'Foobar'
     Then the document has one additional latent style
      And latent_styles['Foobar'] is a latent style


  Scenario: Delete a latent style
    Given a document having known styles
     When I delete a latent style
     Then the document has one fewer latent styles
      And the deleted latent style is not in the latent styles collection
