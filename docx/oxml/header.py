from .xmlchemy import BaseOxmlElement, ZeroOrMore


class CT_Header(BaseOxmlElement):
    """
    ``<w:body>``, the container element for the main document story in
    ``document.xml``.
    """
    p = ZeroOrMore('w:p', successors=())

    # TODO DO THIS METHOD!
    @staticmethod
    def new(partname, content_type):
        """
        Return a new ``<Override>`` element with attributes set to parameter
        values.
        """
        pass
        # xml = '<Override xmlns="%s"/>' % nsmap['ct']
        # override = parse_xml(xml)
        # override.set('PartName', partname)
        # override.set('ContentType', content_type)
        # return override
