# encoding: utf-8

"""
Enumerations related to text in WordprocessingML files
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.enum.base import EnumMember, XmlEnumeration, alias


@alias("WD_FIELDCODE")
class WD_FIELD_TYPE(XmlEnumeration):
    """Specifies the allowable field codes which may be used."""

    __ms_name__ = "WdFieldType"

    __url__ = "https://msdn.microsoft.com/en-us/vba/word-vba/articles/wdfieldtype-enumeration-word"

    __members__ = (
        EnumMember(
            "ADDIN",
            81,
            "Add-in field. Not available through the Field dialog"
            "box. Used to store data that is hidden from the user interface.",
        ),
        EnumMember("ADVANCE", 84, "Advance field."),
        EnumMember("ASK", 38, "Ask field."),
        EnumMember("AUTHOR", 17, "Author field."),
        EnumMember("AUTONUM", 54, "AutoNum field."),
        EnumMember("AUTONUMLEGAL", 53, "AutoNumLgl field."),
        EnumMember("AUTONUMOUTLINE", 52, "AutoNumOut field."),
        EnumMember("AUTOTEXT", 79, "AutoText field."),
        EnumMember("AUTOTEXTLIST", 89, "AutoTextList field."),
        EnumMember("BARCODE", 63, "BarCode field."),
        EnumMember("BIDIOUTLINE", 92, "BidiOutline field."),
        EnumMember("COMMENTS", 19, "Comments field."),
        EnumMember("COMPARE", 80, "Compare field."),
        EnumMember("CREATEDATE", 21, "CreateDate field."),
        EnumMember("DATA", 40, "Data field."),
        EnumMember("DATABASE", 78, "Database field."),
        EnumMember("DATE", 31, "Date field."),
        EnumMember(
            "DDE",
            45,
            "DDE field. No longer available through the Field"
            "dialog box, but supported for documents created in earlier"
            "versions of Word.",
        ),
        EnumMember(
            "DDEAUTO",
            46,
            "DDEAuto field. No longer available through the"
            "Field dialog box, but supported for documents created in earlier"
            "versions of Word.",
        ),
        EnumMember("DISPLAYBARCODE", 99, "DisplayBarcode field."),
        EnumMember("DOCPROPERTY", 85, "DocProperty field."),
        EnumMember("DOCVARIABLE", 64, "DocVariable field."),
        EnumMember("EDITTIME", 25, "EditTime field."),
        EnumMember("EMBED", 58, "Embedded field."),
        EnumMember(
            "EMPTY",
            -1,
            "Empty field. Acts as a placeholder for field content"
            "that has not yet been added. A field added by pressing Ctrl+F9 in"
            "the user interface is an Empty field.",
        ),
        EnumMember("EXPRESSION", 34, "= (Formula) field."),
        EnumMember("FILENAME", 29, "FileName field."),
        EnumMember("FILESIZE", 69, "FileSize field."),
        EnumMember("FILLIN", 39, "Fill-In field."),
        EnumMember(
            "FOOTNOTEREF",
            5,
            "FootnoteRef field. Not available through the"
            "Field dialog box. Inserted programmatically or interactively.",
        ),
        EnumMember("FORMCHECKBOX", 71, "FormCheckBox field."),
        EnumMember("FORMDROPDOWN", 83, "FormDropDown field."),
        EnumMember("FORMTEXTINPUT", 70, "FormText field."),
        EnumMember("FORMULA", 49, "EQ (Equation) field."),
        EnumMember("GLOSSARY", 47, "Glossary field. No longer supported in Word."),
        EnumMember("GOTOBUTTON", 50, "GoToButton field."),
        EnumMember("GREETINGLINE", 94, "GreetingLine field."),
        EnumMember("HTMLACTIVEX", 91, "HTMLActiveX field. Not currently supported."),
        EnumMember("HYPERLINK", 88, "Hyperlink field."),
        EnumMember("IF", 7, "If field."),
        EnumMember(
            "IMPORT",
            55,
            "Import field. Cannot be added through the Field"
            "dialog box, but can be added interactively or through code.",
        ),
        EnumMember(
            "INCLUDE",
            36,
            "Include field. Cannot be added through the Field"
            "dialog box, but can be added interactively or through code.",
        ),
        EnumMember("INCLUDEPICTURE", 67, "IncludePicture field."),
        EnumMember("INCLUDETEXT", 68, "IncludeText field."),
        EnumMember("INDEX", 8, "Index field."),
        EnumMember("INDEXENTRY", 4, "XE (Index Entry) field."),
        EnumMember("INFO", 14, "Info field."),
        EnumMember("KEYWORD", 18, "Keywords field."),
        EnumMember("LASTSAVEDBY", 20, "LastSavedBy field."),
        EnumMember("LINK", 56, "Link field."),
        EnumMember("LISTNUM", 90, "ListNum field."),
        EnumMember("MACROBUTTON", 51, "MacroButton field."),
        EnumMember("MERGEBARCODE", 98, "MergeBarcode field."),
        EnumMember("MERGEFIELD", 59, "MergeField field."),
        EnumMember("MERGEREC", 44, "MergeRec field."),
        EnumMember("MERGESEQ", 75, "MergeSeq field."),
        EnumMember("NEXT", 41, "Next field."),
        EnumMember("NEXTIF", 42, "NextIf field."),
        EnumMember("NOTEREF", 72, "NoteRef field."),
        EnumMember("NUMCHARS", 28, "NumChars field."),
        EnumMember("NUMPAGES", 26, "NumPages field."),
        EnumMember("NUMWORDS", 27, "NumWords field."),
        EnumMember(
            "OCX",
            87,
            "OCX field. Cannot be added through the Field dialog"
            "box, but can be added through code by using the AddOLEControl"
            "method of the Shapes collection or of the InlineShapes collection",
        ),
        EnumMember("PAGE", 33, "Page field."),
        EnumMember("PAGEREF", 37, "PageRef field."),
        EnumMember("PRINT", 48, "Print field."),
        EnumMember("PRINTDATE", 23, "PrintDate field."),
        EnumMember("PRIVATE", 77, "Private field."),
        EnumMember("QUOTE", 35, "Quote field."),
        EnumMember("REF", 3, "Ref field."),
        EnumMember("REFDOC", 11, "RD (Reference Document) field."),
        EnumMember("REVISIONNUM", 24, "RevNum field."),
        EnumMember("SAVEDATE", 22, "SaveDate field."),
        EnumMember("SECTION", 65, "Section field."),
        EnumMember("SECTIONPAGES", 66, "SectionPages field."),
        EnumMember("SEQUENCE", 12, "Seq (Sequence) field."),
        EnumMember("SET", 6, "Set field."),
        EnumMember(
            "SHAPE", 95, "Shape field. Automatically created for any drawn" "picture."
        ),
        EnumMember("SKIPIF", 43, "SkipIf field."),
        EnumMember("STYLEREF", 10, "StyleRef field."),
        EnumMember("SUBJECT", 16, "Subject field."),
        EnumMember(
            "SUBSCRIBER",
            82,
            "Macintosh only. For information about this"
            "constant, consult the language reference Help included with"
            "Microsoft Office Macintosh Edition.",
        ),
        EnumMember("SYMBOL", 57, "Symbol field."),
        EnumMember("TEMPLATE", 30, "Template field."),
        EnumMember("TIME", 32, "Time field."),
        EnumMember("TITLE", 15, "Title field."),
        EnumMember("TOA", 73, "TOA (Table of Authorities) field."),
        EnumMember("TOAENTRY", 74, "TOA (Table of Authorities Entry) field."),
        EnumMember("TOC", 13, "TOC (Table of Contents) field."),
        EnumMember("TOCENTRY", 9, "TOC (Table of Contents Entry) field."),
        EnumMember("USERADDRESS", 62, "UserAddress field."),
        EnumMember("USERINITIALS", 61, "UserInitials field."),
        EnumMember("USERNAME", 60, "UserName field."),
        EnumMember("BIBLIOGRAPHY", 97, "Bibliography field."),
        EnumMember("CITATION", 96, "Citation field."),
        EnumMember(
            "ADDIN",
            81,
            "Add-in field. Not available through the Field dialog"
            "box. Used to store data that is hidden from the user interface.",
        ),
        EnumMember("ADDRESSBLOCK", 93, "AddressBlock field."),
        EnumMember("ADVANCE", 84, "Advance field."),
        EnumMember("ASK", 38, "Ask field."),
        EnumMember("AUTHOR", 17, "Author field."),
        EnumMember("AUTONUM", 54, "AutoNum field."),
        EnumMember("AUTONUMLEGAL", 53, "AutoNumLgl field."),
        EnumMember("AUTONUMOUTLINE", 52, "AutoNumOut field."),
        EnumMember("AUTOTEXT", 79, "AutoText field."),
        EnumMember("AUTOTEXTLIST", 89, "AutoTextList field."),
        EnumMember("BARCODE", 63, "BarCode field."),
        EnumMember("BIDIOUTLINE", 92, "BidiOutline field."),
        EnumMember("COMMENTS", 19, "Comments field."),
        EnumMember("COMPARE", 80, "Compare field."),
        EnumMember("CREATEDATE", 21, "CreateDate field."),
        EnumMember("DATA", 40, "Data field."),
        EnumMember("DATABASE", 78, "Database field."),
        EnumMember("DATE", 31, "Date field."),
        EnumMember(
            "DDE",
            45,
            "DDE field. No longer available through the Field"
            "dialog box, but supported for documents created in earlier"
            "versions of Word.",
        ),
        EnumMember(
            "DDEAUTO",
            46,
            "DDEAuto field. No longer available through the"
            "Field dialog box, but supported for documents created in earlier"
            "versions of Word.",
        ),
        EnumMember("DISPLAYBARCODE", 99, "DisplayBarcode field."),
        EnumMember("DOCPROPERTY", 85, "DocProperty field."),
        EnumMember("DOCVARIABLE", 64, "DocVariable field."),
        EnumMember("EDITTIME", 25, "EditTime field."),
        EnumMember("EMBED", 58, "Embedded field."),
        EnumMember(
            "EMPTY",
            -1,
            "Empty field. Acts as a placeholder for field content"
            "that has not yet been added. A field added by pressing Ctrl+F9 in"
            "the user interface is an Empty field.",
        ),
        EnumMember("EXPRESSION", 34, "= (Formula) field."),
        EnumMember("FILENAME", 29, "FileName field."),
        EnumMember("FILESIZE", 69, "FileSize field."),
        EnumMember("FILLIN", 39, "Fill-In field."),
        EnumMember(
            "FOOTNOTEREF",
            5,
            "FootnoteRef field. Not available through the"
            "Field dialog box. Inserted programmatically or interactively.",
        ),
        EnumMember("FORMCHECKBOX", 71, "FormCheckBox field."),
        EnumMember("FORMDROPDOWN", 83, "FormDropDown field."),
        EnumMember("FORMTEXTINPUT", 70, "FormText field."),
        EnumMember("FORMULA", 49, "EQ (Equation) field."),
        EnumMember("GLOSSARY", 47, "Glossary field. No longer supported in Word."),
        EnumMember("GOTOBUTTON", 50, "GoToButton field."),
        EnumMember("GREETINGLINE", 94, "GreetingLine field."),
        EnumMember("HTMLACTIVEX", 91, "HTMLActiveX field. Not currently supported."),
        EnumMember("HYPERLINK", 88, "Hyperlink field."),
        EnumMember("IF", 7, "If field."),
        EnumMember(
            "IMPORT",
            55,
            "Import field. Cannot be added through the Field"
            "dialog box, but can be added interactively or through code.",
        ),
        EnumMember(
            "INCLUDE",
            36,
            "Include field. Cannot be added through the Field"
            "dialog box, but can be added interactively or through code.",
        ),
        EnumMember("INCLUDEPICTURE", 67, "IncludePicture field."),
        EnumMember("INCLUDETEXT", 68, "IncludeText field."),
        EnumMember("INDEX", 8, "Index field."),
        EnumMember("INDEXENTRY", 4, "XE (Index Entry) field."),
        EnumMember("INFO", 14, "Info field."),
        EnumMember("KEYWORD", 18, "Keywords field."),
        EnumMember("LASTSAVEDBY", 20, "LastSavedBy field."),
        EnumMember("LINK", 56, "Link field."),
        EnumMember("LISTNUM", 90, "ListNum field."),
        EnumMember("MACROBUTTON", 51, "MacroButton field."),
        EnumMember("MERGEBARCODE", 98, "MergeBarcode field."),
        EnumMember("MERGEFIELD", 59, "MergeField field."),
        EnumMember("MERGEREC", 44, "MergeRec field."),
        EnumMember("MERGESEQ", 75, "MergeSeq field."),
        EnumMember("NEXT", 41, "Next field."),
        EnumMember("NEXTIF", 42, "NextIf field."),
        EnumMember("NOTEREF", 72, "NoteRef field."),
        EnumMember("NUMCHARS", 28, "NumChars field."),
        EnumMember("NUMPAGES", 26, "NumPages field."),
        EnumMember("NUMWORDS", 27, "NumWords field."),
        EnumMember(
            "OCX",
            87,
            "OCX field. Cannot be added through the Field dialog"
            "box, but can be added through code by using the AddOLEControl"
            "method of the Shapes collection or of the InlineShapes collection",
        ),
        EnumMember("PAGE", 33, "Page field."),
        EnumMember("PAGEREF", 37, "PageRef field."),
        EnumMember("PRINT", 48, "Print field."),
        EnumMember("PRINTDATE", 23, "PrintDate field."),
        EnumMember("PRIVATE", 77, "Private field."),
        EnumMember("QUOTE", 35, "Quote field."),
        EnumMember("REF", 3, "Ref field."),
        EnumMember("REFDOC", 11, "RD (Reference Document) field."),
        EnumMember("REVISIONNUM", 24, "RevNum field."),
        EnumMember("SAVEDATE", 22, "SaveDate field."),
        EnumMember("SECTION", 65, "Section field."),
        EnumMember("SECTIONPAGES", 66, "SectionPages field."),
        EnumMember("SEQ", 12, "Seq (Sequence) field."),
        EnumMember("SET", 6, "Set field."),
        EnumMember(
            "SHAPE", 95, "Shape field. Automatically created for any drawn" "picture."
        ),
        EnumMember("SKIPIF", 43, "SkipIf field."),
        EnumMember("STYLEREF", 10, "StyleRef field."),
        EnumMember("SUBJECT", 16, "Subject field."),
        EnumMember(
            "SUBSCRIBER",
            82,
            "Macintosh only. For information about this"
            "constant, consult the language reference Help included with"
            "Microsoft Office Macintosh Edition.",
        ),
        EnumMember("SYMBOL", 57, "Symbol field."),
        EnumMember("TEMPLATE", 30, "Template field."),
        EnumMember("TIME", 32, "Time field."),
        EnumMember("TITLE", 15, "Title field."),
        EnumMember("TOA", 73, "TOA (Table of Authorities) field."),
        EnumMember("TOAENTRY", 74, "TOA (Table of Authorities Entry) field."),
        EnumMember("TOC", 13, "TOC (Table of Contents) field."),
        EnumMember("TOCENTRY", 9, "TOC (Table of Contents Entry) field."),
        EnumMember("USERADDRESS", 62, "UserAddress field."),
        EnumMember("USERINITIALS", 61, "UserInitials field."),
        EnumMember("USERNAME", 60, "UserName field."),
        EnumMember("BIBLIOGRAPHY", 97, "Bibliography field."),
        EnumMember("CITATION", 96, "Citation field."),
    )
