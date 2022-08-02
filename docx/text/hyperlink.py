from docx.shared import RGBColor
from ..runcntnr import RunItemContainer
from .run import Run


class Hyperlink(RunItemContainer):
    """
    Proxy object wrapping ``<w:hyperlink>`` element.
    """
    def __init__(self, element, parent):
        super(Hyperlink, self).__init__(element, parent)

    @property
    def anchor(self):
        return self._element.anchor

    @anchor.setter
    def anchor(self, value):
        self._element.anchor = value

    def clear(self):
        self._element.clear_content()
        return self

    @property
    def is_external(self):
        _id = self._element.id
        if _id is None:
            return False
        else:
            return True

    @property
    def target(self):
        if self.is_external:
            return self.relationship_id
        else:
            return self.anchor

    @property
    def relationship_id(self):
        return self._element.id

    @relationship_id.setter
    def relationship_id(self, value):
        self._element.id = value

    @property
    def runs(self):
        """
        Sequence of |Run| instances corresponding to ``<w:r>`` elements in
        this hyperlink.
        """
        return [Run(r, self) for r in self._element.r_lst]

    @classmethod
    def add_hyperlink_styles(cls, document):
        from docx.enum.style import WD_STYLE_TYPE
        from docx.enum.dml import MSO_THEME_COLOR
        styles = document.styles
        try:
            hyperlink_style = styles.get_style_id("Hyperlink", WD_STYLE_TYPE.CHARACTER)
        except (ValueError, KeyError):
            _style = styles.add_style("Hyperlink", WD_STYLE_TYPE.CHARACTER, True)
            _style.base_style = styles["Default Paragraph Font"]
            _style.font.color.rgb = RGBColor.from_string("0563C1")
            _style.font.color.theme_color = MSO_THEME_COLOR.HYPERLINK
            _style.font.underline = True
        else:
            pass