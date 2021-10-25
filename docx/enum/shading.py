"""Enumerations related to shading."""

from __future__ import absolute_import, print_function, unicode_literals

from .base import XmlEnumeration, XmlMappedEnumMember


class WD_SHADING_PATTERN(XmlEnumeration):
    """
    Specifies the shading texture to use for a selected item.

    Example::

        from docx import Document
        from docx.enum.style import WD_SHADING_PATTERN

        doc = Document()
        table = doc.add_table(1,1)
        cell = table.cell(0,0)
        cell.shading.texture = WD_SHADING_PATTERN.DIAGONAL_CROSS
    """

    __ms_name__ = "WdTextureIndex"

    __url__ = "https://docs.microsoft.com/en-us/office/vba/api/word.wdtextureindex"

    __members__ = (
        XmlMappedEnumMember("CLEAR", 1, "clear", "No Pattern."),
        XmlMappedEnumMember(
            "DIAGONAL_CROSS", 8, "diagCross", "Diagonal Cross Pattern."
        ),
        XmlMappedEnumMember(
            "DIAGONAL_STRIPE", 6, "diagStripe", "Diagonal Stripe Pattern."
        ),
        XmlMappedEnumMember(
            "HORIZONTAL_CROSS", 7, "horzCross", "Horizontal Cross Pattern."
        ),
        XmlMappedEnumMember(
            "HORIZONTAL_STRIPE", 3, "horzStripe", "Horizontal Stripe Pattern."
        ),
        XmlMappedEnumMember("NIL", 0, "nil", "No Pattern."),
        XmlMappedEnumMember("PERCENT_10", 16, "pct10", "10% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_12", 17, "pct12", "12.5% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_15", 18, "pct15", "15% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_20", 19, "pct20", "20% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_25", 20, "pct25", "25% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_30", 21, "pct30", "30% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_35", 22, "pct35", "35% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_37", 23, "pct37", "37.5% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_40", 24, "pct40", "40% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_45", 25, "pct45", "45% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_5", 15, "pct5", "5% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_50", 26, "pct50", "50% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_55", 27, "pct55", "55% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_60", 28, "pct60", "60% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_62", 29, "pct62", "62.5% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_65", 30, "pct65", "65% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_70", 31, "pct70", "70% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_75", 32, "pct75", "75% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_80", 33, "pct80", "80% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_85", 34, "pct85", "85% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_87", 35, "pct87", "87.5% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_90", 36, "pct90", "90% Fill Pattern."),
        XmlMappedEnumMember("PERCENT_95", 37, "pct95", "95% Fill Pattern."),
        XmlMappedEnumMember(
            "REVERSE_DIAGONAL_STRIPE",
            5,
            "reverseDiagStripe",
            "Reverse Diagonal Stripe Pattern.",
        ),
        XmlMappedEnumMember("SOLID", 2, "solid", "100% Fill Pattern."),
        XmlMappedEnumMember(
            "THIN_DIAGONAL_CROSS", 14, "thinDiagCross", "Thin Diagonal Cross Pattern."
        ),
        XmlMappedEnumMember(
            "THIN_DIAGONAL_STRIPE",
            12,
            "thinDiagStripe",
            "Thin Diagonal Stripe Pattern.",
        ),
        XmlMappedEnumMember(
            "THIN_HORIZONTAL_CROSS",
            13,
            "thinHorzCross",
            "Thin Horizontal Cross Pattern.",
        ),
        XmlMappedEnumMember(
            "THIN_HORIZONTAL_STRIPE",
            9,
            "thinHorzStripe",
            "Thin Horizontal Stripe Pattern.",
        ),
        XmlMappedEnumMember(
            "THIN_REVERSEDIAGONAL_STRIPE",
            11,
            "thinReverseDiagStripe",
            "Thin Reverse Diagonal Stripe Pattern.",
        ),
        XmlMappedEnumMember(
            "THIN_VERTICAL_STRIPE",
            10,
            "thinVertStripe",
            "Thin Vertical Stripe Pattern.",
        ),
        XmlMappedEnumMember(
            "VERTICAL_STRIPE", 4, "vertStripe", "Vertical Stripe Pattern."
        ),
    )
