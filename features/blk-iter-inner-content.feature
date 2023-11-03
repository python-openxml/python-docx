Feature: Iterate paragraphs and tables in document-order
  In order to access paragraphs and tables in the same order they appear in the document
  As a developer using python-docx
  I need the ability to iterate the inner-content of a block-item-container


  Scenario: Document.iter_inner_content()
    Given a Document object with paragraphs and tables
     Then document.iter_inner_content() produces the block-items in document order


  Scenario: Header.iter_inner_content()
    Given a Header object with paragraphs and tables
     Then header.iter_inner_content() produces the block-items in document order


  Scenario: Footer.iter_inner_content()
    Given a Footer object with paragraphs and tables
     Then footer.iter_inner_content() produces the block-items in document order


  Scenario: _Cell.iter_inner_content()
    Given a _Cell object with paragraphs and tables
     Then cell.iter_inner_content() produces the block-items in document order
