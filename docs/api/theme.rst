Theme fonts
===========

The document theme contains major (heading) and minor (body) font families.
Changing these fonts affects text that references the corresponding theme slots.
It does not apply direct formatting to runs or rewrite style definitions.

.. code-block:: python

    document.theme_fonts.name = "Company fonts"
    document.theme_fonts.major_latin = "Aptos Display"
    document.theme_fonts.minor_latin = "Aptos"

These properties control Latin fonts. East Asian, complex-script, supplemental
fonts, theme colors, and effects are preserved. Optional metrics associated with
the old Latin typeface are removed when that typeface is assigned.

Access creates a complete default theme if the document has none. An existing
malformed or incomplete font scheme raises ``ValueError``.

``ThemeFonts`` objects
----------------------

.. autoclass:: docx.theme.ThemeFonts
   :members:

Binding styles to theme fonts
-----------------------------

Templates can contain literal font names that override inherited theme fonts.
Use ``Font.theme_font`` to bind Latin text to the major or minor family. This
removes conflicting Latin literals from that font definition.

.. code-block:: python

    document.styles.default_font.theme_font = "minor"
    document.styles["Normal"].font.theme_font = "minor"
    for level in range(1, 7):
        style = document.styles[f"Heading {level}"]
        style.font.theme_font = "major"
        if style.linked_style is not None:
            style.linked_style.font.theme_font = "major"

The linked character style handles applying the heading style to selected text.
It is independent of the paragraph style. ``linked_style`` is read-only and
returns ``None`` when the link or its target is absent.

``Styles.default_font`` exposes character defaults at the root of the style
hierarchy. It creates missing default containers when accessed. Properties set
on individual styles or runs can override those defaults.

``theme_font`` reads local references only. It returns ``None`` for absent or
mixed Latin theme families. It does not compute the effective inherited font.
Assigning ``None`` removes Latin theme references and preserves literal names.
Existing ``Font.name`` behavior is unchanged. For a fixed monospace font, use:

.. code-block:: python

    code_style.font.theme_font = None
    code_style.font.name = "Consolas"

No runs need individual font assignments. Later changes to the theme affect
existing and newly created paragraphs using these styles.
