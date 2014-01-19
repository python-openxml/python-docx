Feature: Characterize an image file
  In order add a picture to a document
  As a programmer using the advanced python-docx API
  I need a way to determine the image content type and size

  @wip
  Scenario Outline: Characterize an image file
    Given the image file '<filename>'
     When I construct an image using the image path
     Then the image has content type '<mime_type>'
      And the image is <cx> pixels wide
      And the image is <cy> pixels high
      And the image has <horz_dpi> horizontal dpi
      And the image has <vert_dpi> vertical dpi

   Examples: Image file characteristics
     | filename | mime_type | cx | cy | horz_dpi | vert_dpi |
     | test.png | image/png | 11 | 22 |   333    |   444    |
