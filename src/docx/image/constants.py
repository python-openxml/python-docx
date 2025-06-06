"""Constants specific the the image sub-package."""


class JPEG_MARKER_CODE:
    """JPEG marker codes."""

    TEM = b"\x01"
    DHT = b"\xc4"
    DAC = b"\xcc"
    JPG = b"\xc8"

    SOF0 = b"\xc0"
    SOF1 = b"\xc1"
    SOF2 = b"\xc2"
    SOF3 = b"\xc3"
    SOF5 = b"\xc5"
    SOF6 = b"\xc6"
    SOF7 = b"\xc7"
    SOF9 = b"\xc9"
    SOFA = b"\xca"
    SOFB = b"\xcb"
    SOFD = b"\xcd"
    SOFE = b"\xce"
    SOFF = b"\xcf"

    RST0 = b"\xd0"
    RST1 = b"\xd1"
    RST2 = b"\xd2"
    RST3 = b"\xd3"
    RST4 = b"\xd4"
    RST5 = b"\xd5"
    RST6 = b"\xd6"
    RST7 = b"\xd7"

    SOI = b"\xd8"
    EOI = b"\xd9"
    SOS = b"\xda"
    DQT = b"\xdb"  # Define Quantization Table(s)
    DNL = b"\xdc"
    DRI = b"\xdd"
    DHP = b"\xde"
    EXP = b"\xdf"

    APP0 = b"\xe0"
    APP1 = b"\xe1"
    APP2 = b"\xe2"
    APP3 = b"\xe3"
    APP4 = b"\xe4"
    APP5 = b"\xe5"
    APP6 = b"\xe6"
    APP7 = b"\xe7"
    APP8 = b"\xe8"
    APP9 = b"\xe9"
    APPA = b"\xea"
    APPB = b"\xeb"
    APPC = b"\xec"
    APPD = b"\xed"
    APPE = b"\xee"
    APPF = b"\xef"

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
        b"\xc0": "SOF0",
        b"\xc2": "SOF2",
        b"\xc4": "DHT",
        b"\xda": "SOS",  # start of scan
        b"\xd8": "SOI",  # start of image
        b"\xd9": "EOI",  # end of image
        b"\xdb": "DQT",
        b"\xe0": "APP0",
        b"\xe1": "APP1",
        b"\xe2": "APP2",
        b"\xed": "APP13",
        b"\xee": "APP14",
    }

    @classmethod
    def is_standalone(cls, marker_code):
        return marker_code in cls.STANDALONE_MARKERS


class MIME_TYPE:
    """Image content types."""

    BMP = "image/bmp"
    GIF = "image/gif"
    JPEG = "image/jpeg"
    PNG = "image/png"
    TIFF = "image/tiff"


class PNG_CHUNK_TYPE:
    """PNG chunk type names."""

    IHDR = "IHDR"
    pHYs = "pHYs"
    IEND = "IEND"


class TIFF_FLD_TYPE:
    """Tag codes for TIFF Image File Directory (IFD) entries."""

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


class TIFF_TAG:
    """Tag codes for TIFF Image File Directory (IFD) entries."""

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
