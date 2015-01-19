Feature: Access latent styles for a document
  In order to operate on the latent styles for a document
  As a developer using python-docx
  I need access to the latent styles collection


  Scenario: Access latent styles collection
    Given the style collection of a document
     Then styles.latent_styles is the LatentStyles object for the document
      And len(latent_styles) is 137


  Scenario: Access latent style in collection
     Given a latent style collection
      Then I can iterate over the latent styles
       And I can access a latent style by name
