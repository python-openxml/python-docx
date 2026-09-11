"""Styles object, container for all objects in the styles part."""

from __future__ import annotations

from warnings import warn

from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.styles import CT_Styles
from docx.shared import ElementProxy, Pt
from docx.styles import BabelFish
from docx.styles.latent import LatentStyles
from docx.styles.style import BaseStyle, StyleFactory


class Styles(ElementProxy):
    """Provides access to the styles defined in a document.

    Accessed using the :attr:`.Document.styles` property. Supports ``len()``, iteration,
    and dictionary-style access by style name.
    """

    def __init__(self, styles: CT_Styles):
        super().__init__(styles)
        self._element = styles

    def __contains__(self, name):
        """Enables `in` operator on style name."""
        internal_name = BabelFish.ui2internal(name)
        return any(style.name_val == internal_name for style in self._element.style_lst)

    def __getitem__(self, key: str):
        """Enables dictionary-style access by UI name.

        Lookup by style id is deprecated, triggers a warning, and will be removed in a
        near-future release.
        """
        style_elm = self._element.get_by_name(BabelFish.ui2internal(key))
        if style_elm is not None:
            return StyleFactory(style_elm)

        style_elm = self._element.get_by_id(key)
        if style_elm is not None:
            msg = "style lookup by style_id is deprecated. Use style name as key instead."
            warn(msg, UserWarning, stacklevel=2)
            return StyleFactory(style_elm)

        raise KeyError("no style with name '%s'" % key)

    def __iter__(self):
        return (StyleFactory(style) for style in self._element.style_lst)

    def __len__(self):
        return len(self._element.style_lst)

    def add_style(self, name, style_type, builtin=False):
        """Return a newly added style object of `style_type` and identified by `name`.

        A builtin style can be defined by passing True for the optional `builtin`
        argument.
        """
        style_name = BabelFish.ui2internal(name)
        if style_name in self:
            raise ValueError("document already contains style '%s'" % name)
        style = self._element.add_style_of_type(style_name, style_type, builtin)
        return StyleFactory(style)

    def default(self, style_type: WD_STYLE_TYPE):
        """Return the default style for `style_type` or |None| if no default is defined
        for that type (not common)."""
        style = self._element.default_for(style_type)
        if style is None:
            return None
        return StyleFactory(style)

    def get_by_id(self, style_id: str | None, style_type: WD_STYLE_TYPE):
        """Return the style of `style_type` matching `style_id`.

        Returns the default for `style_type` if `style_id` is not found or is |None|, or
        if the style having `style_id` is not of `style_type`.
        """
        if style_id is None:
            return self.default(style_type)
        return self._get_by_id(style_id, style_type)

    def get_style_id(self, style_or_name, style_type):
        """Return the id of the style corresponding to `style_or_name`, or |None| if
        `style_or_name` is |None|.

        If `style_or_name` is not a style object, the style is looked up using
        `style_or_name` as a style name, raising |ValueError| if no style with that name
        is defined. Raises |ValueError| if the target style is not of `style_type`.
        """
        if style_or_name is None:
            return None
        elif isinstance(style_or_name, BaseStyle):
            return self._get_style_id_from_style(style_or_name, style_type)
        else:
            return self._get_style_id_from_name(style_or_name, style_type)

    @property
    def latent_styles(self):
        """A |LatentStyles| object providing access to the default behaviors for latent
        styles and the collection of |_LatentStyle| objects that define overrides of
        those defaults for a particular named latent style."""
        return LatentStyles(self._element.get_or_add_latentStyles())

    def _get_by_id(self, style_id: str | None, style_type: WD_STYLE_TYPE):
        """Return the style of `style_type` matching `style_id`.

        Returns the default for `style_type` if `style_id` is not found or if the style
        having `style_id` is not of `style_type`.
        """
        style = self._element.get_by_id(style_id) if style_id else None
        if style is None or style.type != style_type:
            return self.default(style_type)
        return StyleFactory(style)

    def _ensure_comment_reference_style(self) -> None:
        """Add the built-in 'CommentReference' character style if not present.

        `Document.add_comment()` writes `<w:rStyle w:val="CommentReference"/>` into the
        reference run but never adds the corresponding style definition to styles.xml.
        Word silently tolerates the dangling reference, but the reference mark then
        inherits default run formatting instead of the intended 8-pt "annotation
        reference" appearance.  This method adds the style once per document, skipping
        the work on subsequent calls.
        """
        if self._element.get_by_id("CommentReference") is not None:
            return
        style_elm = self._element.add_style_of_type(
            "annotation reference", WD_STYLE_TYPE.CHARACTER, True
        )
        # The auto-generated styleId from the name would be "annotationreference";
        # override it to match the id that the reference run already uses.
        style_elm.styleId = "CommentReference"
        style_elm.basedOn_val = "DefaultParagraphFont"
        style_elm.uiPriority_val = 99
        style_elm.semiHidden_val = True
        style_elm.unhideWhenUsed_val = True
        rPr = style_elm.get_or_add_rPr()
        rPr.sz_val = Pt(8)

    def _get_style_id_from_name(self, style_name: str, style_type: WD_STYLE_TYPE) -> str | None:
        """Return the id of the style of `style_type` corresponding to `style_name`.

        Returns |None| if that style is the default style for `style_type`. Raises
        |ValueError| if the named style is not found in the document or does not match
        `style_type`.
        """
        return self._get_style_id_from_style(self[style_name], style_type)

    def _get_style_id_from_style(self, style: BaseStyle, style_type: WD_STYLE_TYPE) -> str | None:
        """Id of `style`, or |None| if it is the default style of `style_type`.

        Raises |ValueError| if style is not of `style_type`.
        """
        if style.type != style_type:
            raise ValueError("assigned style is type %s, need type %s" % (style.type, style_type))
        if style == self.default(style_type):
            return None
        return style.style_id
