from .blkcntnr import BlockItemContainer


# TODO figure out if this needed?


class Header(BlockItemContainer):
    """
    Proxy object wrapping ``<w:p>`` element.
    """
    def __init__(self, header_elm, parent):
        super(Header, self).__init__(header_elm, parent)

    # add paragraph inherited from parent
    # add image needs to be added I think?
