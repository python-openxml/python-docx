from ..shared import Parented

class Comment(Parented):
    """[summary]

    :param Parented: [description]
    :type Parented: [type]
    """
    def __init__(self, com, parent):
        super(Comment, self).__init__(parent)
        self._com = self._element = self.element = com
    
    @property
    def paragraph(self):
        return self.element.paragraph
    
    @property
    def text(self):
        return self.element.paragraph.text
    
    @text.setter
    def text(self, text):
        self.element.paragraph.text = text