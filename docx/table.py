# encoding: utf-8

"""
The |Table| object and related proxy classes.
"""


class Table(object):
    """
    Proxy class for a WordprocessingML ``<w:tbl>`` element.
    """
    def __init__(self, tbl_elm):
        super(Table, self).__init__()
        self._tbl = tbl_elm
