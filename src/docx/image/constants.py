# encoding: utf-8

"""
Constants specific the the image sub-package
"""


class JPEG_MARKER_CODE(object):
    """
    JPEG marker codes
    """

    TEM = b"\x01"
    DHT = b"\xC4"
    DAC = b"\xCC"
    JPG = b"\xC8"

    SOF0 = b"\xC0"
    SOF1 = b"\xC1"
    SOF2 = b"\xC2"
    SOF3 = b"\xC3"
    SOF5 = b"\xC5"
    SOF6 = b"\xC6"
    SOF7 = b"\xC7"
    SOF9 = b"\xC9"
    SOFA = b"\xCA"
    SOFB = b"\xCB"
    SOFD = b"\xCD"
    SOFE = b"\xCE"
    SOFF = b"\xCF"

    RST0 = b"\xD0"
    RST1 = b"\xD1"
    RST2 = b"\xD2"
    RST3 = b"\xD3"
    RST4 = b"\xD4"
    RST5 = b"\xD5"
    RST6 = b"\xD6"
    RST7 = b"\xD7"

    SOI = b"\xD8"
    EOI = b"\xD9"
    SOS = b"\xDA"
    DQT = b"\xDB"  # Define Quantization Table(s)
    DNL = b"\xDC"
    DRI = b"\xDD"
    DHP = b"\xDE"
    EXP = b"\xDF"

    APP0 = b"\xE0"
    APP1 = b"\xE1"
    APP2 = b"\xE2"
    APP3 = b"\xE3"
    APP4 = b"\xE4"
    APP5 = b"\xE5"
    APP6 = b"\xE6"
    APP7 = b"\xE7"
    APP8 = b"\xE8"
    APP9 = b"\xE9"
    APPA = b"\xEA"
    APPB = b"\xEB"
    APPC = b"\xEC"
    APPD = b"\xED"
    APPE = b"\xEE"
    APPF = b"\xEF"

    STANDALONE_MARKERS = (TEM, SOI, EOI, RST0, RST1, RST2, RST3, RST4, RST5, RST6, RST7)

    SOF_MARKER_CODES = (
        SOF0,
        SOF1,
        SOF2,
        SOF3,
        SOF5,
        SOF6,
        SOF7,
        SOF9,
        SOFA,
        SOFB,
        SOFD,
        SOFE,
        SOFF,
    )

    marker_names = {
        b"\x00": "UNKNOWN",
        b"\xC0": "SOF0",
        b"\xC2": "SOF2",
        b"\xC4": "DHT",
        b"\xDA": "SOS",  # start of scan
        b"\xD8": "SOI",  # start of image
        b"\xD9": "EOI",  # end of image
        b"\xDB": "DQT",
        b"\xE0": "APP0",
        b"\xE1": "APP1",
        b"\xE2": "APP2",
        b"\xED": "APP13",
        b"\xEE": "APP14",
    }

    @classmethod
    def is_standalone(cls, marker_code):
        return marker_code in cls.STANDALONE_MARKERS


class MIME_TYPE(object):
    """
    Image content types
    """

    BMP = "image/bmp"
    GIF = "image/gif"
    JPEG = "image/jpeg"
    PNG = "image/png"
    TIFF = "image/tiff"


class PNG_CHUNK_TYPE(object):
    """
    PNG chunk type names
    """

    IHDR = "IHDR"
    pHYs = "pHYs"
    IEND = "IEND"


class TIFF_FLD_TYPE(object):
    """
    Tag codes for TIFF Image File Directory (IFD) entries.
    """

    BYTE = 1
    ASCII = 2
    SHORT = 3
    LONG = 4
    RATIONAL = 5

    field_type_names = {
        1: "BYTE",
        2: "ASCII char",
        3: "SHORT",
        4: "LONG",
        5: "RATIONAL",
    }


TIFF_FLD = TIFF_FLD_TYPE


class TIFF_TAG(object):
    """
    Tag codes for TIFF Image File Directory (IFD) entries.
    """

    IMAGE_WIDTH = 0x0100
    IMAGE_LENGTH = 0x0101
    X_RESOLUTION = 0x011A
    Y_RESOLUTION = 0x011B
    RESOLUTION_UNIT = 0x0128

    tag_names = {
        0x00FE: "NewSubfileType",
        0x0100: "ImageWidth",
        0x0101: "ImageLength",
        0x0102: "BitsPerSample",
        0x0103: "Compression",
        0x0106: "PhotometricInterpretation",
        0x010E: "ImageDescription",
        0x010F: "Make",
        0x0110: "Model",
        0x0111: "StripOffsets",
        0x0112: "Orientation",
        0x0115: "SamplesPerPixel",
        0x0117: "StripByteCounts",
        0x011A: "XResolution",
        0x011B: "YResolution",
        0x011C: "PlanarConfiguration",
        0x0128: "ResolutionUnit",
        0x0131: "Software",
        0x0132: "DateTime",
        0x0213: "YCbCrPositioning",
        0x8769: "ExifTag",
        0x8825: "GPS IFD",
        0xC4A5: "PrintImageMatching",
    }
