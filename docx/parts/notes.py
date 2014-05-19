from ..opc.package import Part
from ..oxml.shared import oxml_fromstring
from ..shared import lazyproperty
from ..text import Paragraph


class EndnotesPart(Part):

    def __init__(self, partname, content_type, endnotes_elm, package):
        super(EndnotesPart, self).__init__(
            partname, content_type, package=package
        )
        self._element = endnotes_elm
    
    @classmethod
    def load(cls, partname, content_type, blob, package):
        """
        Provides PartFactory interface for loading a numbering part from
        a WML package.
        """
        endnotes_elm = oxml_fromstring(blob)
        return cls(partname, content_type, endnotes_elm, package)

    def get_note(self, note_id):
        if not hasattr(self, '_notes_map'):
            self._notes_map = dict((n.id, n) for n in self.notes)
        return self._notes_map[note_id]
    
    @property
    def notes(self):
        return [Note(n) for n in self._element.notes_lst]
    
    
class Note(object):
    
    def __init__(self, el):
        self._element = el
        self.id = el.id
        self.type = el.type
        
    @property
    def paragraphs(self):
        return [Paragraph(p) for p in self._element.p_lst]
