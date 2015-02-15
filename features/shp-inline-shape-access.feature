Feature: Access inline shape in inline shape collection
  In order to operate on an inline shape
  As a developer using python-docx
  I need a way to access each inline shape in the inline shape collection


  Scenario: Access shape in inline shape collection
     Given an inline shape collection containing five shapes
      Then the length of the inline shape collection is 5
       And I can iterate over the inline shape collection
       And I can access each inline shape by index


  Scenario Outline: Identify type of inline shape
     Given an inline shape known to be <shape of type>
      Then its inline shape type is <shape type>

   Examples: Inline shapes of recognized types
     | shape of type        | shape type                     |
     | an embedded picture  | WD_INLINE_SHAPE.PICTURE        |
     | a linked picture     | WD_INLINE_SHAPE.LINKED_PICTURE |
     | a link+embed picture | WD_INLINE_SHAPE.LINKED_PICTURE |
     | a smart art diagram  | WD_INLINE_SHAPE.SMART_ART      |
     | a chart              | WD_INLINE_SHAPE.CHART          |
