"""Constant values related to the Open Packaging Convention.

In particular it includes content types and relationship types.
"""


class CONTENT_TYPE:
    """Content type URIs (like MIME-types) that specify a part's format."""

    BMP = "image/bmp"
    DML_CHART = "application/vnd.openxmlformats-officedocument.drawingml.chart+xml"
    DML_CHARTSHAPES = "application/vnd.openxmlformats-officedocument.drawingml.chartshapes+xml"
    DML_DIAGRAM_COLORS = "application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml"
    DML_DIAGRAM_DATA = "application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml"
    DML_DIAGRAM_LAYOUT = "application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml"
    DML_DIAGRAM_STYLE = "application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml"
    GIF = "image/gif"
    JPEG = "image/jpeg"
    MS_PHOTO = "image/vnd.ms-photo"
    OFC_CUSTOM_PROPERTIES = "application/vnd.openxmlformats-officedocument.custom-properties+xml"
    OFC_CUSTOM_XML_PROPERTIES = (
        "application/vnd.openxmlformats-officedocument.customXmlProperties+xml"
    )
    OFC_DRAWING = "application/vnd.openxmlformats-officedocument.drawing+xml"
    OFC_EXTENDED_PROPERTIES = (
        "application/vnd.openxmlformats-officedocument.extended-properties+xml"
    )
    OFC_OLE_OBJECT = "application/vnd.openxmlformats-officedocument.oleObject"
    OFC_PACKAGE = "application/vnd.openxmlformats-officedocument.package"
    OFC_THEME = "application/vnd.openxmlformats-officedocument.theme+xml"
    OFC_THEME_OVERRIDE = "application/vnd.openxmlformats-officedocument.themeOverride+xml"
    OFC_VML_DRAWING = "application/vnd.openxmlformats-officedocument.vmlDrawing"
    OPC_CORE_PROPERTIES = "application/vnd.openxmlformats-package.core-properties+xml"
    OPC_DIGITAL_SIGNATURE_CERTIFICATE = (
        "application/vnd.openxmlformats-package.digital-signature-certificate"
    )
    OPC_DIGITAL_SIGNATURE_ORIGIN = "application/vnd.openxmlformats-package.digital-signature-origin"
    OPC_DIGITAL_SIGNATURE_XMLSIGNATURE = (
        "application/vnd.openxmlformats-package.digital-signature-xmlsignature+xml"
    )
    OPC_RELATIONSHIPS = "application/vnd.openxmlformats-package.relationships+xml"
    PML_COMMENTS = "application/vnd.openxmlformats-officedocument.presentationml.comments+xml"
    PML_COMMENT_AUTHORS = (
        "application/vnd.openxmlformats-officedocument.presentationml.commentAuthors+xml"
    )
    PML_HANDOUT_MASTER = (
        "application/vnd.openxmlformats-officedocument.presentationml.handoutMaster+xml"
    )
    PML_NOTES_MASTER = (
        "application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"
    )
    PML_NOTES_SLIDE = "application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"
    PML_PRESENTATION_MAIN = (
        "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"
    )
    PML_PRES_PROPS = "application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"
    PML_PRINTER_SETTINGS = (
        "application/vnd.openxmlformats-officedocument.presentationml.printerSettings"
    )
    PML_SLIDE = "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
    PML_SLIDESHOW_MAIN = (
        "application/vnd.openxmlformats-officedocument.presentationml.slideshow.main+xml"
    )
    PML_SLIDE_LAYOUT = (
        "application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"
    )
    PML_SLIDE_MASTER = (
        "application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"
    )
    PML_SLIDE_UPDATE_INFO = (
        "application/vnd.openxmlformats-officedocument.presentationml.slideUpdateInfo+xml"
    )
    PML_TABLE_STYLES = (
        "application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"
    )
    PML_TAGS = "application/vnd.openxmlformats-officedocument.presentationml.tags+xml"
    PML_TEMPLATE_MAIN = (
        "application/vnd.openxmlformats-officedocument.presentationml.template.main+xml"
    )
    PML_VIEW_PROPS = "application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"
    PNG = "image/png"
    SML_CALC_CHAIN = "application/vnd.openxmlformats-officedocument.spreadsheetml.calcChain+xml"
    SML_CHARTSHEET = "application/vnd.openxmlformats-officedocument.spreadsheetml.chartsheet+xml"
    SML_COMMENTS = "application/vnd.openxmlformats-officedocument.spreadsheetml.comments+xml"
    SML_CONNECTIONS = "application/vnd.openxmlformats-officedocument.spreadsheetml.connections+xml"
    SML_CUSTOM_PROPERTY = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.customProperty"
    )
    SML_DIALOGSHEET = "application/vnd.openxmlformats-officedocument.spreadsheetml.dialogsheet+xml"
    SML_EXTERNAL_LINK = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.externalLink+xml"
    )
    SML_PIVOT_CACHE_DEFINITION = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.pivotCacheDefinition+xml"
    )
    SML_PIVOT_CACHE_RECORDS = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.pivotCacheRecords+xml"
    )
    SML_PIVOT_TABLE = "application/vnd.openxmlformats-officedocument.spreadsheetml.pivotTable+xml"
    SML_PRINTER_SETTINGS = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.printerSettings"
    )
    SML_QUERY_TABLE = "application/vnd.openxmlformats-officedocument.spreadsheetml.queryTable+xml"
    SML_REVISION_HEADERS = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.revisionHeaders+xml"
    )
    SML_REVISION_LOG = "application/vnd.openxmlformats-officedocument.spreadsheetml.revisionLog+xml"
    SML_SHARED_STRINGS = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"
    )
    SML_SHEET = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    SML_SHEET_MAIN = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"
    SML_SHEET_METADATA = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheetMetadata+xml"
    )
    SML_STYLES = "application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"
    SML_TABLE = "application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml"
    SML_TABLE_SINGLE_CELLS = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.tableSingleCells+xml"
    )
    SML_TEMPLATE_MAIN = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.template.main+xml"
    )
    SML_USER_NAMES = "application/vnd.openxmlformats-officedocument.spreadsheetml.userNames+xml"
    SML_VOLATILE_DEPENDENCIES = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.volatileDependencies+xml"
    )
    SML_WORKSHEET = "application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"
    TIFF = "image/tiff"
    WML_COMMENTS = "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"
    WML_DOCUMENT = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    WML_DOCUMENT_GLOSSARY = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document.glossary+xml"
    )
    WML_DOCUMENT_MAIN = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
    )
    WML_ENDNOTES = "application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml"
    WML_FONT_TABLE = "application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"
    WML_FOOTER = "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"
    WML_FOOTNOTES = "application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"
    WML_HEADER = "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"
    WML_NUMBERING = "application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"
    WML_PRINTER_SETTINGS = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.printerSettings"
    )
    WML_SETTINGS = "application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"
    WML_STYLES = "application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"
    WML_WEB_SETTINGS = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml"
    )
    XML = "application/xml"
    X_EMF = "image/x-emf"
    X_FONTDATA = "application/x-fontdata"
    X_FONT_TTF = "application/x-font-ttf"
    X_WMF = "image/x-wmf"


class NAMESPACE:
    """Constant values for OPC XML namespaces."""

    DML_WORDPROCESSING_DRAWING = (
        "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
    )
    OFC_RELATIONSHIPS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    OPC_RELATIONSHIPS = "http://schemas.openxmlformats.org/package/2006/relationships"
    OPC_CONTENT_TYPES = "http://schemas.openxmlformats.org/package/2006/content-types"
    WML_MAIN = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


class RELATIONSHIP_TARGET_MODE:
    """Open XML relationship target modes."""

    EXTERNAL = "External"
    INTERNAL = "Internal"


class RELATIONSHIP_TYPE:
    AUDIO = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/audio"
    A_F_CHUNK = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/aFChunk"
    CALC_CHAIN = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/calcChain"
    CERTIFICATE = (
        "http://schemas.openxmlformats.org/package/2006/relationships/digital-signature/certificate"
    )
    CHART = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart"
    CHARTSHEET = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/chartsheet"
    CHART_USER_SHAPES = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/chartUserShapes"
    )
    COMMENTS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"
    COMMENT_AUTHORS = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/commentAuthors"
    )
    CONNECTIONS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/connections"
    CONTROL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/control"
    CORE_PROPERTIES = (
        "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties"
    )
    CUSTOM_PROPERTIES = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties"
    )
    CUSTOM_PROPERTY = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/customProperty"
    )
    CUSTOM_XML = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/customXml"
    CUSTOM_XML_PROPS = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/customXmlProps"
    )
    DIAGRAM_COLORS = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramColors"
    )
    DIAGRAM_DATA = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramData"
    DIAGRAM_LAYOUT = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramLayout"
    )
    DIAGRAM_QUICK_STYLE = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramQuickStyle"
    )
    DIALOGSHEET = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/dialogsheet"
    DRAWING = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing"
    ENDNOTES = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/endnotes"
    EXTENDED_PROPERTIES = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties"
    )
    EXTERNAL_LINK = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/externalLink"
    )
    FONT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font"
    FONT_TABLE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable"
    FOOTER = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer"
    FOOTNOTES = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes"
    GLOSSARY_DOCUMENT = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/glossaryDocument"
    )
    HANDOUT_MASTER = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/handoutMaster"
    )
    HEADER = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/header"
    HYPERLINK = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
    IMAGE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
    NOTES_MASTER = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster"
    NOTES_SLIDE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide"
    NUMBERING = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering"
    OFFICE_DOCUMENT = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
    )
    OLE_OBJECT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/oleObject"
    ORIGIN = "http://schemas.openxmlformats.org/package/2006/relationships/digital-signature/origin"
    PACKAGE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/package"
    PIVOT_CACHE_DEFINITION = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/pivotCacheDefinition"
    )
    PIVOT_CACHE_RECORDS = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
        "/spreadsheetml/pivotCacheRecords"
    )
    PIVOT_TABLE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/pivotTable"
    PRES_PROPS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps"
    PRINTER_SETTINGS = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/printerSettings"
    )
    QUERY_TABLE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/queryTable"
    REVISION_HEADERS = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/revisionHeaders"
    )
    REVISION_LOG = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/revisionLog"
    SETTINGS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings"
    SHARED_STRINGS = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings"
    )
    SHEET_METADATA = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/sheetMetadata"
    )
    SIGNATURE = (
        "http://schemas.openxmlformats.org/package/2006/relationships/digital-signature/signature"
    )
    SLIDE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
    SLIDE_LAYOUT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout"
    SLIDE_MASTER = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster"
    SLIDE_UPDATE_INFO = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideUpdateInfo"
    )
    STYLES = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"
    TABLE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/table"
    TABLE_SINGLE_CELLS = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableSingleCells"
    )
    TABLE_STYLES = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles"
    TAGS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/tags"
    THEME = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme"
    THEME_OVERRIDE = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/themeOverride"
    )
    THUMBNAIL = "http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail"
    USERNAMES = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/usernames"
    VIDEO = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/video"
    VIEW_PROPS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/viewProps"
    VML_DRAWING = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/vmlDrawing"
    VOLATILE_DEPENDENCIES = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/volatileDependencies"
    )
    WEB_SETTINGS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/webSettings"
    WORKSHEET_SOURCE = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheetSource"
    )
    XML_MAPS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/xmlMaps"
