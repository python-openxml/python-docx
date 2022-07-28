import os

CURDIR = os.path.dirname(os.path.abspath(__file__))

def get_multi_header_and_footer_document():
    """
    Returns fully defined path to a word document that contains:
    * Two sections
        * Created in word using Layout -> Breaks -> Next Page
    * Each section contains a single paragraph and run with text 
      content of "Section X"
    * Each section has its own header and footer. Each header 
      and footer contains text content of "Header X" or "Footer X"
    """
    return os.path.join(CURDIR, "multi-header-footer.docx")