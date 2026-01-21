from docx.oxml import parse_xml
from docx.text.paragraph import Paragraph
from docx.text.run import Run

class DescribeTrackedChanges:
    def it_includes_insertions_in_paragraph_text(self):
        """
        paragraph.text includes text within <w:ins> tags.
        """
        xml = (
            '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">'
            '  <w:r><w:t>Start </w:t></w:r>'
            '  <w:ins w:id="1" w:author="Me" w:date="2023-01-01T00:00:00Z">'
            '    <w:r><w:t>Inserted</w:t></w:r>'
            '  </w:ins>'
            '  <w:r><w:t> End</w:t></w:r>'
            '</w:p>'
        )
        p = Paragraph(parse_xml(xml), None)
        # Expected: "Start Inserted End"
        # Before Fix: "Start  End"
        assert p.text == "Start Inserted End"

    def it_excludes_deletions_in_paragraph_text(self):
        """
        paragraph.text still excludes text within <w:del> tags (standard behavior).
        """
        xml = (
            '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '  <w:r><w:t>Start </w:t></w:r>'
            '  <w:del w:id="2" w:author="Me" w:date="2023-01-01T00:00:00Z">'
            '    <w:r><w:delText>Deleted</w:delText></w:r>'
        '  </w:del>'
        '  <w:r><w:t>End</w:t></w:r>'
        '</w:p>'
        )
        p = Paragraph(parse_xml(xml), None)
        assert p.text == "Start End"

    def it_includes_moved_text_destination(self):
        """
        paragraph.text includes text within <w:moveTo> tags (treated as accepted/visible).
        """
        xml = (
            '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '  <w:r><w:t>Start </w:t></w:r>'
            '  <w:moveTo w:id="3" w:author="Me" w:date="2023-01-01T00:00:00Z">'
            '    <w:r><w:t>Moved Text</w:t></w:r>'
            '  </w:moveTo>'
            '  <w:r><w:t> End</w:t></w:r>'
            '</w:p>'
        )
        p = Paragraph(parse_xml(xml), None)
        assert p.text == "Start Moved Text End"
