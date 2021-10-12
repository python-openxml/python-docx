# encoding: utf-8

"""
Enumerations related to text in WordprocessingML files
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.enum.base import (
    XmlEnumeration,
    XmlMappedEnumMember,
    alias,
)


@alias("WD_FIELDCODE")
class WD_FIELD_TYPE(XmlEnumeration):
    """Specifies the allowable field codes which may be used."""

    __ms_name__ = "WdFieldType"

    __url__ = "https://msdn.microsoft.com/en-us/vba/word-vba/articles/wdfieldtype-enumeration-word"

    __members__ = (
        XmlMappedEnumMember(
            "ADDIN",
            81,
            "ADDIN",
            "Add-in field. Not available through the Field dialog"
            "box. Used to store data that is hidden from the user interface.",
        ),
        XmlMappedEnumMember("ADVANCE", 84, "ADVANCE", "Advance field."),
        XmlMappedEnumMember("ASK", 38, "ASK", "Ask field."),
        XmlMappedEnumMember("AUTHOR", 17, "AUTHOR", "Author field."),
        XmlMappedEnumMember("AUTONUM", 54, "AUTONUM", "AutoNum field."),
        XmlMappedEnumMember("AUTONUMLEGAL", 53, "AUTONUMLEGAL", "AutoNumLgl field."),
        XmlMappedEnumMember(
            "AUTONUMOUTLINE", 52, "AUTONUMOUTLINE", "AutoNumOut field."
        ),
        XmlMappedEnumMember("AUTOTEXT", 79, "AUTOTEXT", "AutoText field."),
        XmlMappedEnumMember("AUTOTEXTLIST", 89, "AUTOTEXTLIST", "AutoTextList field."),
        XmlMappedEnumMember("BARCODE", 63, "BARCODE", "BarCode field."),
        XmlMappedEnumMember("BIDIOUTLINE", 92, "BIDIOUTLINE", "BidiOutline field."),
        XmlMappedEnumMember("COMMENTS", 19, "COMMENTS", "Comments field."),
        XmlMappedEnumMember("COMPARE", 80, "COMPARE", "Compare field."),
        XmlMappedEnumMember("CREATEDATE", 21, "CREATEDATE", "CreateDate field."),
        XmlMappedEnumMember("DATA", 40, "DATA", "Data field."),
        XmlMappedEnumMember("DATABASE", 78, "DATABASE", "Database field."),
        XmlMappedEnumMember("DATE", 31, "DATE", "Date field."),
        XmlMappedEnumMember(
            "DDE",
            45,
            "DDE",
            "DDE field. No longer available through the Field"
            "dialog box, but supported for documents created in earlier"
            "versions of Word.",
        ),
        XmlMappedEnumMember(
            "DDEAUTO",
            46,
            "DDEAUTO",
            "DDEAuto field. No longer available through the"
            "Field dialog box, but supported for documents created in earlier"
            "versions of Word.",
        ),
        XmlMappedEnumMember(
            "DISPLAYBARCODE", 99, "DISPLAYBARCODE", "DisplayBarcode field."
        ),
        XmlMappedEnumMember("DOCPROPERTY", 85, "DOCPROPERTY", "DocProperty field."),
        XmlMappedEnumMember("DOCVARIABLE", 64, "DOCVARIABLE", "DocVariable field."),
        XmlMappedEnumMember("EDITTIME", 25, "EDITTIME", "EditTime field."),
        XmlMappedEnumMember("EMBED", 58, "EMBED", "Embedded field."),
        XmlMappedEnumMember(
            "EMPTY",
            -1,
            "EMPTY",
            "Empty field. Acts as a placeholder for field content"
            "that has not yet been added. A field added by pressing Ctrl+F9 in"
            "the user interface is an Empty field.",
        ),
        XmlMappedEnumMember("EXPRESSION", 34, "EXPRESSION", "= (Formula) field."),
        XmlMappedEnumMember("FILENAME", 29, "FILENAME", "FileName field."),
        XmlMappedEnumMember("FILESIZE", 69, "FILESIZE", "FileSize field."),
        XmlMappedEnumMember("FILLIN", 39, "FILLIN", "Fill-In field."),
        XmlMappedEnumMember(
            "FOOTNOTEREF",
            5,
            "FOOTNOTEREF",
            "FootnoteRef field. Not available through the"
            "Field dialog box. Inserted programmatically or interactively.",
        ),
        XmlMappedEnumMember("FORMCHECKBOX", 71, "FORMCHECKBOX", "FormCheckBox field."),
        XmlMappedEnumMember("FORMDROPDOWN", 83, "FORMDROPDOWN", "FormDropDown field."),
        XmlMappedEnumMember("FORMTEXTINPUT", 70, "FORMTEXTINPUT", "FormText field."),
        XmlMappedEnumMember("FORMULA", 49, "FORMULA", "EQ (Equation) field."),
        XmlMappedEnumMember(
            "GLOSSARY", 47, "GLOSSARY", "Glossary field. No longer supported in Word."
        ),
        XmlMappedEnumMember("GOTOBUTTON", 50, "GOTOBUTTON", "GoToButton field."),
        XmlMappedEnumMember("GREETINGLINE", 94, "GREETINGLINE", "GreetingLine field."),
        XmlMappedEnumMember(
            "HTMLACTIVEX",
            91,
            "HTMLACTIVEX",
            "HTMLActiveX field. Not currently supported.",
        ),
        XmlMappedEnumMember("HYPERLINK", 88, "HYPERLINK", "Hyperlink field."),
        XmlMappedEnumMember("IF", 7, "IF", "If field."),
        XmlMappedEnumMember(
            "IMPORT",
            55,
            "IMPORT",
            "Import field. Cannot be added through the Field"
            "dialog box, but can be added interactively or through code.",
        ),
        XmlMappedEnumMember(
            "INCLUDE",
            36,
            " INCLUDE",
            "Include field. Cannot be added through the Field"
            "dialog box, but can be added interactively or through code.",
        ),
        XmlMappedEnumMember(
            "INCLUDEPICTURE", 67, "INCLUDEPICTURE", "IncludePicture field."
        ),
        XmlMappedEnumMember("INCLUDETEXT", 68, "INCLUDETEXT", "IncludeText field."),
        XmlMappedEnumMember("INDEX", 8, "INDEX", "Index field."),
        XmlMappedEnumMember("INDEXENTRY", 4, "INDEXENTRY", "XE (Index Entry) field."),
        XmlMappedEnumMember("INFO", 14, "INFO", "Info field."),
        XmlMappedEnumMember("KEYWORD", 18, "KEYWORD", "Keywords field."),
        XmlMappedEnumMember("LASTSAVEDBY", 20, "LASTSAVEDBY", "LastSavedBy field."),
        XmlMappedEnumMember("LINK", 56, "LINK", "Link field."),
        XmlMappedEnumMember("LISTNUM", 90, "LISTNUM", "ListNum field."),
        XmlMappedEnumMember("MACROBUTTON", 51, "MACROBUTTON", "MacroButton field."),
        XmlMappedEnumMember("MERGEBARCODE", 98, "MERGEBARCODE", "MergeBarcode field."),
        XmlMappedEnumMember("MERGEFIELD", 59, "MERGEFIELD", "MergeField field."),
        XmlMappedEnumMember("MERGEREC", 44, "MERGEREC", "MergeRec field."),
        XmlMappedEnumMember("MERGESEQ", 75, "MERGESEQ", "MergeSeq field."),
        XmlMappedEnumMember("NEXT", 41, "NEXT", "Next field."),
        XmlMappedEnumMember("NEXTIF", 42, "NEXTIF", "NextIf field."),
        XmlMappedEnumMember("NOTEREF", 72, "NOTEREF", "NoteRef field."),
        XmlMappedEnumMember("NUMCHARS", 28, "NUMCHARS", "NumChars field."),
        XmlMappedEnumMember("NUMPAGES", 26, "NUMPAGES", "NumPages field."),
        XmlMappedEnumMember("NUMWORDS", 27, "NUMWORDS", "NumWords field."),
        XmlMappedEnumMember(
            "OCX",
            87,
            "OCX",
            "OCX field. Cannot be added through the Field dialog"
            "box, but can be added through code by using the AddOLEControl"
            "method of the Shapes collection or of the InlineShapes collection",
        ),
        XmlMappedEnumMember("PAGE", 33, "PAGE", "Page field."),
        XmlMappedEnumMember("PAGEREF", 37, "PAGEREF", "PageRef field."),
        XmlMappedEnumMember("PRINT", 48, "PRINT", "Print field."),
        XmlMappedEnumMember("PRINTDATE", 23, "PRINTDATE", "PrintDate field."),
        XmlMappedEnumMember("PRIVATE", 77, "PRIVATE", "Private field."),
        XmlMappedEnumMember("QUOTE", 35, "QUOTE", "Quote field."),
        XmlMappedEnumMember("REF", 3, "REF", "Ref field."),
        XmlMappedEnumMember("REFDOC", 11, "REFDOC", "RD (Reference Document) field."),
        XmlMappedEnumMember("REVISIONNUM", 24, "REVISIONNUM", "RevNum field."),
        XmlMappedEnumMember("SAVEDATE", 22, "SAVEDATE", "SaveDate field."),
        XmlMappedEnumMember("SECTION", 65, "SECTION", "Section field."),
        XmlMappedEnumMember("SECTIONPAGES", 66, "SECTIONPAGES", "SectionPages field."),
        XmlMappedEnumMember("SEQUENCE", 12, "SEQUENCE", "Seq (Sequence) field."),
        XmlMappedEnumMember("SET", 6, "SET", "Set field."),
        XmlMappedEnumMember(
            "SHAPE",
            95,
            "SHAPE",
            "Shape field. Automatically created for any drawn" "picture.",
        ),
        XmlMappedEnumMember("SKIPIF", 43, "SKIPIF", "SkipIf field."),
        XmlMappedEnumMember("STYLEREF", 10, "STYLEREF", "StyleRef field."),
        XmlMappedEnumMember("SUBJECT", 16, "SUBJECT", "Subject field."),
        XmlMappedEnumMember(
            "SUBSCRIBER",
            82,
            "SUBSCRIBER",
            "Macintosh only. For information about this"
            "constant, consult the language reference Help included with"
            "Microsoft Office Macintosh Edition.",
        ),
        XmlMappedEnumMember("SYMBOL", 57, "SYMBOL", "Symbol field."),
        XmlMappedEnumMember("TEMPLATE", 30, "TEMPLATE", "Template field."),
        XmlMappedEnumMember("TIME", 32, "TIME", "Time field."),
        XmlMappedEnumMember("TITLE", 15, "TITLE", "Title field."),
        XmlMappedEnumMember("TOA", 73, "TOA", "TOA (Table of Authorities) field."),
        XmlMappedEnumMember(
            "TOAENTRY", 74, "TOAENTRY", "TOA (Table of Authorities Entry) field."
        ),
        XmlMappedEnumMember("TOC", 13, "TOC", "TOC (Table of Contents) field."),
        XmlMappedEnumMember(
            "TOCENTRY", 9, "TOCENTRY", "TOC (Table of Contents Entry) field."
        ),
        XmlMappedEnumMember("USERADDRESS", 62, "USERADDRESS", "UserAddress field."),
        XmlMappedEnumMember("USERINITIALS", 61, "USERINITIALS", "UserInitials field."),
        XmlMappedEnumMember("USERNAME", 60, "USERNAME", "UserName field."),
        XmlMappedEnumMember("BIBLIOGRAPHY", 97, "BIBLIOGRAPHY", "Bibliography field."),
        XmlMappedEnumMember("CITATION", 96, "CITATION", "Citation field."),
        XmlMappedEnumMember(
            "ADDIN",
            81,
            "ADDIN",
            "Add-in field. Not available through the Field dialog"
            "box. Used to store data that is hidden from the user interface.",
        ),
        XmlMappedEnumMember("ADDRESSBLOCK", 93, "ADDRESSBLOCK", "AddressBlock field."),
        XmlMappedEnumMember("ADVANCE", 84, "ADVANCE", "Advance field."),
        XmlMappedEnumMember("ASK", 38, "ASK", "Ask field."),
        XmlMappedEnumMember("AUTHOR", 17, "AUTHOR", "Author field."),
        XmlMappedEnumMember("AUTONUM", 54, "AUTONUM", "AutoNum field."),
        XmlMappedEnumMember("AUTONUMLEGAL", 53, "AUTONUMLEGAL", "AutoNumLgl field."),
        XmlMappedEnumMember(
            "AUTONUMOUTLINE", 52, "AUTONUMOUTLINE", "AutoNumOut field."
        ),
        XmlMappedEnumMember("AUTOTEXT", 79, "AUTOTEXT", "AutoText field."),
        XmlMappedEnumMember("AUTOTEXTLIST", 89, "AUTOTEXTLIST", "AutoTextList field."),
        XmlMappedEnumMember("BARCODE", 63, "BARCODE", "BarCode field."),
        XmlMappedEnumMember("BIDIOUTLINE", 92, "BIDIOUTLINE", "BidiOutline field."),
        XmlMappedEnumMember("COMMENTS", 19, "COMMENTS", "Comments field."),
        XmlMappedEnumMember("COMPARE", 80, "COMPARE", "Compare field."),
        XmlMappedEnumMember("CREATEDATE", 21, "CREATEDATE", "CreateDate field."),
        XmlMappedEnumMember("DATA", 40, "DATA", "Data field."),
        XmlMappedEnumMember("DATABASE", 78, "DATABASE", "Database field."),
        XmlMappedEnumMember("DATE", 31, "DATE", "Date field."),
        XmlMappedEnumMember(
            "DDE",
            45,
            "DDE",
            "DDE field. No longer available through the Field"
            "dialog box, but supported for documents created in earlier"
            "versions of Word.",
        ),
        XmlMappedEnumMember(
            "DDEAUTO",
            46,
            "DDEAUTO",
            "DDEAuto field. No longer available through the"
            "Field dialog box, but supported for documents created in earlier"
            "versions of Word.",
        ),
        XmlMappedEnumMember(
            "DISPLAYBARCODE", 99, "DISPLAYBARCODE", "DisplayBarcode field."
        ),
        XmlMappedEnumMember("DOCPROPERTY", 85, "DOCPROPERTY", "DocProperty field."),
        XmlMappedEnumMember("DOCVARIABLE", 64, "DOCVARIABLE", "DocVariable field."),
        XmlMappedEnumMember("EDITTIME", 25, "EDITTIME", "EditTime field."),
        XmlMappedEnumMember("EMBED", 58, "EMBED", "Embedded field."),
        XmlMappedEnumMember(
            "EMPTY",
            -1,
            "EMPTY",
            "Empty field. Acts as a placeholder for field content"
            "that has not yet been added. A field added by pressing Ctrl+F9 in"
            "the user interface is an Empty field.",
        ),
        XmlMappedEnumMember("EXPRESSION", 34, "EXPRESSION", "= (Formula) field."),
        XmlMappedEnumMember("FILENAME", 29, "FILENAME", "FileName field."),
        XmlMappedEnumMember("FILESIZE", 69, "FILESIZE", "FileSize field."),
        XmlMappedEnumMember("FILLIN", 39, "FILLIN", "Fill-In field."),
        XmlMappedEnumMember(
            "FOOTNOTEREF",
            5,
            "FOOTNOTEREF",
            "FootnoteRef field. Not available through the"
            "Field dialog box. Inserted programmatically or interactively.",
        ),
        XmlMappedEnumMember("FORMCHECKBOX", 71, "FORMCHECKBOX", "FormCheckBox field."),
        XmlMappedEnumMember("FORMDROPDOWN", 83, "FORMDROPDOWN", "FormDropDown field."),
        XmlMappedEnumMember("FORMTEXTINPUT", 70, "FORMTEXTINPUT", "FormText field."),
        XmlMappedEnumMember("FORMULA", 49, "FORMULA", "EQ (Equation) field."),
        XmlMappedEnumMember(
            "GLOSSARY", 47, "GLOSSARY", "Glossary field. No longer supported in Word."
        ),
        XmlMappedEnumMember("GOTOBUTTON", 50, "GOTOBUTTON", "GoToButton field."),
        XmlMappedEnumMember("GREETINGLINE", 94, "GREETINGLINE", "GreetingLine field."),
        XmlMappedEnumMember(
            "HTMLACTIVEX",
            91,
            "HTMLACTIVEX",
            "HTMLActiveX field. Not currently supported.",
        ),
        XmlMappedEnumMember("HYPERLINK", 88, "HYPERLINK", "Hyperlink field."),
        XmlMappedEnumMember("IF", 7, "IF", "If field."),
        XmlMappedEnumMember(
            "IMPORT",
            55,
            "IMPORT",
            "Import field. Cannot be added through the Field"
            "dialog box, but can be added interactively or through code.",
        ),
        XmlMappedEnumMember(
            "INCLUDE",
            36,
            "INCLUDE",
            "Include field. Cannot be added through the Field"
            "dialog box, but can be added interactively or through code.",
        ),
        XmlMappedEnumMember(
            "INCLUDEPICTURE", 67, "INCLUDEPICTURE", "IncludePicture field."
        ),
        XmlMappedEnumMember("INCLUDETEXT", 68, "INCLUDETEXT", "IncludeText field."),
        XmlMappedEnumMember("INDEX", 8, "INDEX", "Index field."),
        XmlMappedEnumMember("INDEXENTRY", 4, "INDEXENTRY", "XE (Index Entry) field."),
        XmlMappedEnumMember("INFO", 14, "INFO", "Info field."),
        XmlMappedEnumMember("KEYWORD", 18, "KEYWORD", "Keywords field."),
        XmlMappedEnumMember("LASTSAVEDBY", 20, "LASTSAVEDBY", "LastSavedBy field."),
        XmlMappedEnumMember("LINK", 56, "LINK", "Link field."),
        XmlMappedEnumMember("LISTNUM", 90, "LISTNUM", "ListNum field."),
        XmlMappedEnumMember("MACROBUTTON", 51, "MACROBUTTON", "MacroButton field."),
        XmlMappedEnumMember("MERGEBARCODE", 98, "MERGEBARCODE", "MergeBarcode field."),
        XmlMappedEnumMember("MERGEFIELD", 59, "MERGEFIELD", "MergeField field."),
        XmlMappedEnumMember("MERGEREC", 44, "MERGEREC", "MergeRec field."),
        XmlMappedEnumMember("MERGESEQ", 75, "MERGESEQ", "MergeSeq field."),
        XmlMappedEnumMember("NEXT", 41, "NEXT", "Next field."),
        XmlMappedEnumMember("NEXTIF", 42, "NEXTIF", "NextIf field."),
        XmlMappedEnumMember("NOTEREF", 72, "NOTEREF", "NoteRef field."),
        XmlMappedEnumMember("NUMCHARS", 28, "NUMCHARS", "NumChars field."),
        XmlMappedEnumMember("NUMPAGES", 26, "NUMPAGES", "NumPages field."),
        XmlMappedEnumMember("NUMWORDS", 27, "NUMWORDS", "NumWords field."),
        XmlMappedEnumMember(
            "OCX",
            87,
            "OCX",
            "OCX field. Cannot be added through the Field dialog"
            "box, but can be added through code by using the AddOLEControl"
            "method of the Shapes collection or of the InlineShapes collection",
        ),
        XmlMappedEnumMember("PAGE", 33, "PAGE", "Page field."),
        XmlMappedEnumMember("PAGEREF", 37, "PAGEREF", "PageRef field."),
        XmlMappedEnumMember("PRINT", 48, "PRINT", "Print field."),
        XmlMappedEnumMember("PRINTDATE", 23, "PRINTDATE", "PrintDate field."),
        XmlMappedEnumMember("PRIVATE", 77, "PRIVATE", "Private field."),
        XmlMappedEnumMember("QUOTE", 35, "QUOTE", "Quote field."),
        XmlMappedEnumMember("REF", 3, "REF", "Ref field."),
        XmlMappedEnumMember("REFDOC", 11, "REFDOC", "RD (Reference Document) field."),
        XmlMappedEnumMember("REVISIONNUM", 24, "REVISIONNUM", "RevNum field."),
        XmlMappedEnumMember("SAVEDATE", 22, "SAVEDATE", "SaveDate field."),
        XmlMappedEnumMember("SECTION", 65, "SECTION", "Section field."),
        XmlMappedEnumMember("SECTIONPAGES", 66, "SECTIONPAGES", "SectionPages field."),
        XmlMappedEnumMember("SEQ", 12, "SEQ", "Seq (Sequence) field."),
        XmlMappedEnumMember("SET", 6, "SET", "Set field."),
        XmlMappedEnumMember(
            "SHAPE",
            95,
            "SHAPE",
            "Shape field. Automatically created for any drawn" "picture.",
        ),
        XmlMappedEnumMember("SKIPIF", 43, "SKIPIF", "SkipIf field."),
        XmlMappedEnumMember("STYLEREF", 10, "STYLEREF", "StyleRef field."),
        XmlMappedEnumMember("SUBJECT", 16, "SUBJECT", "Subject field."),
        XmlMappedEnumMember(
            "SUBSCRIBER",
            82,
            "SUBSCRIBER",
            "Macintosh only. For information about this"
            "constant, consult the language reference Help included with"
            "Microsoft Office Macintosh Edition.",
        ),
        XmlMappedEnumMember("SYMBOL", 57, "SYMBOL", "Symbol field."),
        XmlMappedEnumMember("TEMPLATE", 30, "TEMPLATE", "Template field."),
        XmlMappedEnumMember("TIME", 32, "TIME", "Time field."),
        XmlMappedEnumMember("TITLE", 15, "TITLE", "Title field."),
        XmlMappedEnumMember("TOA", 73, "TOA", "TOA (Table of Authorities) field."),
        XmlMappedEnumMember(
            "TOAENTRY", 74, "TOAENTRY", "TOA (Table of Authorities Entry) field."
        ),
        XmlMappedEnumMember("TOC", 13, "TOC", "TOC (Table of Contents) field."),
        XmlMappedEnumMember(
            "TOCENTRY", 9, "TOCENTRY", "TOC (Table of Contents Entry) field."
        ),
        XmlMappedEnumMember("USERADDRESS", 62, "USERADDRESS", "UserAddress field."),
        XmlMappedEnumMember("USERINITIALS", 61, "USERINITIALS", "UserInitials field."),
        XmlMappedEnumMember("USERNAME", 60, "USERNAME", "UserName field."),
        XmlMappedEnumMember("BIBLIOGRAPHY", 97, "BIBLIOGRAPHY", "Bibliography field."),
        XmlMappedEnumMember("CITATION", 96, "CITATION", "Citation field."),
    )
