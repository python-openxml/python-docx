Feature: Characterize an image file
  In order add a picture to a document
  As a programmer using the advanced python-docx API
  I need a way to determine the image content type and size

  Scenario Outline: Characterize an image file
    Given the image file '<filename>'
     When I construct an image using the image path
     Then the image has content type '<mime_type>'
      And the image is <cx> pixels wide
      And the image is <cy> pixels high
      And the image has <horz_dpi> horizontal dpi
      And the image has <vert_dpi> vertical dpi

   Examples: Image file characteristics
     | filename         | mime_type  |  cx  |  cy  | horz_dpi | vert_dpi |
     | test.png         | image/png  |  901 | 1350 |   150    |   150    |
     | monty-truth.png  | image/png  |  150 |  214 |    72    |    72    |
     | jfif-300-dpi.jpg | image/jpeg | 1504 | 1936 |   300    |   300    |
     | lena_std.jpg     | image/jpeg |  512 |  512 |    72    |    72    |
