"""DrawingML-related objects are in this subpackage."""

from __future__ import annotations

from docx import types as t
from docx.oxml.drawing import CT_Drawing
from docx.shared import Parented


class Drawing(Parented):
    """Container for a DrawingML object."""

    def __init__(self, drawing: CT_Drawing, parent: t.ProvidesStoryPart):
        super().__init__(parent)
        self._parent = parent
        self._drawing = self._element = drawing
