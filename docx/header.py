from .blkcntnr import BlockItemContainer


class Header(BlockItemContainer):
    """
    Proxy object wrapping ``<w:p>`` element.
    """
    def __init__(self, header_elm, parent, part):
        super(Header, self).__init__(header_elm, parent)
        self._part = part

    @property
    def part(self):
        return self._part

    @property
    def styles(self):
        """
        A |Styles| object providing access to the styles in this document.
        """
        return self._part.styles

    @property
    def inline_shapes(self):
        """
        An |InlineShapes| object providing access to the inline shapes in
        this document. An inline shape is a graphical object, such as
        a picture, contained in a run of text and behaving like a character
        glyph, being flowed like other text in a paragraph.
        """
        return self._part.inline_shapes


class Footer(Header):
    """
    Same as header atm
    """
    pass
