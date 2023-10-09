"""Unit test suite for docx.image.tiff module"""

import io

import pytest

from docx.image.constants import MIME_TYPE, TIFF_TAG
from docx.image.helpers import BIG_ENDIAN, LITTLE_ENDIAN, StreamReader
from docx.image.tiff import (
    Tiff,
    _AsciiIfdEntry,
    _IfdEntries,
    _IfdEntry,
    _IfdEntryFactory,
    _IfdParser,
    _LongIfdEntry,
    _RationalIfdEntry,
    _ShortIfdEntry,
    _TiffParser,
)

from ..unitutil.mock import (
    ANY,
    call,
    class_mock,
    function_mock,
    initializer_mock,
    instance_mock,
    loose_mock,
    method_mock,
)


class DescribeTiff:
    def it_can_construct_from_a_tiff_stream(
        self, stream_, _TiffParser_, tiff_parser_, Tiff__init_
    ):
        px_width, px_height = 111, 222
        horz_dpi, vert_dpi = 333, 444
        tiff_parser_.px_width = px_width
        tiff_parser_.px_height = px_height
        tiff_parser_.horz_dpi = horz_dpi
        tiff_parser_.vert_dpi = vert_dpi

        tiff = Tiff.from_stream(stream_)

        _TiffParser_.parse.assert_called_once_with(stream_)
        Tiff__init_.assert_called_once_with(
            ANY, px_width, px_height, horz_dpi, vert_dpi
        )
        assert isinstance(tiff, Tiff)

    def it_knows_its_content_type(self):
        tiff = Tiff(None, None, None, None)
        assert tiff.content_type == MIME_TYPE.TIFF

    def it_knows_its_default_ext(self):
        tiff = Tiff(None, None, None, None)
        assert tiff.default_ext == "tiff"

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def Tiff__init_(self, request):
        return initializer_mock(request, Tiff)

    @pytest.fixture
    def _TiffParser_(self, request, tiff_parser_):
        _TiffParser_ = class_mock(request, "docx.image.tiff._TiffParser")
        _TiffParser_.parse.return_value = tiff_parser_
        return _TiffParser_

    @pytest.fixture
    def tiff_parser_(self, request):
        return instance_mock(request, _TiffParser)

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, io.BytesIO)


class Describe_TiffParser:
    def it_can_parse_the_properties_from_a_tiff_stream(
        self,
        stream_,
        _make_stream_reader_,
        _IfdEntries_,
        ifd0_offset_,
        stream_rdr_,
        _TiffParser__init_,
        ifd_entries_,
    ):
        tiff_parser = _TiffParser.parse(stream_)

        _make_stream_reader_.assert_called_once_with(stream_)
        _IfdEntries_.from_stream.assert_called_once_with(stream_rdr_, ifd0_offset_)
        _TiffParser__init_.assert_called_once_with(ANY, ifd_entries_)
        assert isinstance(tiff_parser, _TiffParser)

    def it_makes_a_stream_reader_to_help_parse(self, mk_stream_rdr_fixture):
        stream, StreamReader_, endian, stream_rdr_ = mk_stream_rdr_fixture
        stream_rdr = _TiffParser._make_stream_reader(stream)
        StreamReader_.assert_called_once_with(stream, endian)
        assert stream_rdr is stream_rdr_

    def it_knows_image_width_and_height_after_parsing(self):
        px_width, px_height = 42, 24
        entries = {
            TIFF_TAG.IMAGE_WIDTH: px_width,
            TIFF_TAG.IMAGE_LENGTH: px_height,
        }
        ifd_entries = _IfdEntries(entries)
        tiff_parser = _TiffParser(ifd_entries)
        assert tiff_parser.px_width == px_width
        assert tiff_parser.px_height == px_height

    def it_knows_the_horz_and_vert_dpi_after_parsing(self, dpi_fixture):
        tiff_parser, expected_horz_dpi, expected_vert_dpi = dpi_fixture
        assert tiff_parser.horz_dpi == expected_horz_dpi
        assert tiff_parser.vert_dpi == expected_vert_dpi

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            (1, 150, 240, 72, 72),
            (2, 42, 24, 42, 24),
            (3, 100, 200, 254, 508),
            (2, None, None, 72, 72),
            (None, 96, 100, 96, 100),
        ]
    )
    def dpi_fixture(self, request):
        resolution_unit, x_resolution, y_resolution = request.param[:3]
        expected_horz_dpi, expected_vert_dpi = request.param[3:]

        entries = {}
        if resolution_unit is not None:
            entries[TIFF_TAG.RESOLUTION_UNIT] = resolution_unit
        if x_resolution is not None:
            entries[TIFF_TAG.X_RESOLUTION] = x_resolution
        if y_resolution is not None:
            entries[TIFF_TAG.Y_RESOLUTION] = y_resolution

        tiff_parser = _TiffParser(entries)
        return tiff_parser, expected_horz_dpi, expected_vert_dpi

    @pytest.fixture
    def _IfdEntries_(self, request, ifd_entries_):
        _IfdEntries_ = class_mock(request, "docx.image.tiff._IfdEntries")
        _IfdEntries_.from_stream.return_value = ifd_entries_
        return _IfdEntries_

    @pytest.fixture
    def ifd_entries_(self, request):
        return instance_mock(request, _IfdEntries)

    @pytest.fixture
    def ifd0_offset_(self, request):
        return instance_mock(request, int)

    @pytest.fixture
    def _make_stream_reader_(self, request, stream_rdr_):
        return method_mock(
            request,
            _TiffParser,
            "_make_stream_reader",
            autospec=False,
            return_value=stream_rdr_,
        )

    @pytest.fixture(
        params=[
            (b"MM\x00*", BIG_ENDIAN),
            (b"II*\x00", LITTLE_ENDIAN),
        ]
    )
    def mk_stream_rdr_fixture(self, request, StreamReader_, stream_rdr_):
        bytes_, endian = request.param
        stream = io.BytesIO(bytes_)
        return stream, StreamReader_, endian, stream_rdr_

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, io.BytesIO)

    @pytest.fixture
    def StreamReader_(self, request, stream_rdr_):
        return class_mock(
            request, "docx.image.tiff.StreamReader", return_value=stream_rdr_
        )

    @pytest.fixture
    def stream_rdr_(self, request, ifd0_offset_):
        stream_rdr_ = instance_mock(request, StreamReader)
        stream_rdr_.read_long.return_value = ifd0_offset_
        return stream_rdr_

    @pytest.fixture
    def _TiffParser__init_(self, request):
        return initializer_mock(request, _TiffParser)


class Describe_IfdEntries:
    def it_can_construct_from_a_stream_and_offset(
        self,
        stream_,
        offset_,
        _IfdParser_,
        ifd_parser_,
        _IfdEntries__init_,
        ifd_entry_,
        ifd_entry_2_,
    ):
        ifd_parser_.iter_entries.return_value = [ifd_entry_, ifd_entry_2_]
        entries_ = {1: 42, 2: 24}

        ifd_entries = _IfdEntries.from_stream(stream_, offset_)

        _IfdParser_.assert_called_once_with(stream_, offset_)
        _IfdEntries__init_.assert_called_once_with(ANY, entries_)
        assert isinstance(ifd_entries, _IfdEntries)

    def it_has_basic_mapping_semantics(self):
        key, value = 1, "foobar"
        entries = {key: value}
        ifd_entries = _IfdEntries(entries)
        assert key in ifd_entries
        assert ifd_entries[key] == value

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def ifd_entry_(self, request):
        return instance_mock(request, _IfdEntry, tag=1, value=42)

    @pytest.fixture
    def ifd_entry_2_(self, request):
        return instance_mock(request, _IfdEntry, tag=2, value=24)

    @pytest.fixture
    def _IfdEntries__init_(self, request):
        return initializer_mock(request, _IfdEntries)

    @pytest.fixture
    def _IfdParser_(self, request, ifd_parser_):
        return class_mock(
            request, "docx.image.tiff._IfdParser", return_value=ifd_parser_
        )

    @pytest.fixture
    def ifd_parser_(self, request):
        return instance_mock(request, _IfdParser)

    @pytest.fixture
    def offset_(self, request):
        return instance_mock(request, int)

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, io.BytesIO)


class Describe_IfdParser:
    def it_can_iterate_through_the_directory_entries_in_an_IFD(self, iter_fixture):
        (
            ifd_parser,
            _IfdEntryFactory_,
            stream_rdr,
            offsets,
            expected_entries,
        ) = iter_fixture
        entries = list(ifd_parser.iter_entries())
        assert _IfdEntryFactory_.call_args_list == [
            call(stream_rdr, offsets[0]),
            call(stream_rdr, offsets[1]),
        ]
        assert entries == expected_entries

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def ifd_entry_(self, request):
        return instance_mock(request, _IfdEntry, tag=1, value=42)

    @pytest.fixture
    def ifd_entry_2_(self, request):
        return instance_mock(request, _IfdEntry, tag=2, value=24)

    @pytest.fixture
    def _IfdEntryFactory_(self, request, ifd_entry_, ifd_entry_2_):
        return function_mock(
            request,
            "docx.image.tiff._IfdEntryFactory",
            side_effect=[ifd_entry_, ifd_entry_2_],
        )

    @pytest.fixture
    def iter_fixture(self, _IfdEntryFactory_, ifd_entry_, ifd_entry_2_):
        stream_rdr = StreamReader(io.BytesIO(b"\x00\x02"), BIG_ENDIAN)
        offsets = [2, 14]
        ifd_parser = _IfdParser(stream_rdr, offset=0)
        expected_entries = [ifd_entry_, ifd_entry_2_]
        return (ifd_parser, _IfdEntryFactory_, stream_rdr, offsets, expected_entries)


class Describe_IfdEntryFactory:
    def it_constructs_the_right_class_for_a_given_ifd_entry(self, fixture):
        stream_rdr, offset, entry_cls_, ifd_entry_ = fixture
        ifd_entry = _IfdEntryFactory(stream_rdr, offset)
        entry_cls_.from_stream.assert_called_once_with(stream_rdr, offset)
        assert ifd_entry is ifd_entry_

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            (b"\x66\x66\x00\x01", "BYTE"),
            (b"\x66\x66\x00\x02", "ASCII"),
            (b"\x66\x66\x00\x03", "SHORT"),
            (b"\x66\x66\x00\x04", "LONG"),
            (b"\x66\x66\x00\x05", "RATIONAL"),
            (b"\x66\x66\x00\x06", "CUSTOM"),
        ]
    )
    def fixture(
        self,
        request,
        ifd_entry_,
        _IfdEntry_,
        _AsciiIfdEntry_,
        _ShortIfdEntry_,
        _LongIfdEntry_,
        _RationalIfdEntry_,
    ):
        bytes_, entry_type = request.param
        entry_cls_ = {
            "BYTE": _IfdEntry_,
            "ASCII": _AsciiIfdEntry_,
            "SHORT": _ShortIfdEntry_,
            "LONG": _LongIfdEntry_,
            "RATIONAL": _RationalIfdEntry_,
            "CUSTOM": _IfdEntry_,
        }[entry_type]
        stream_rdr = StreamReader(io.BytesIO(bytes_), BIG_ENDIAN)
        offset = 0
        return stream_rdr, offset, entry_cls_, ifd_entry_

    @pytest.fixture
    def ifd_entry_(self, request):
        return instance_mock(request, _IfdEntry)

    @pytest.fixture
    def _IfdEntry_(self, request, ifd_entry_):
        _IfdEntry_ = class_mock(request, "docx.image.tiff._IfdEntry")
        _IfdEntry_.from_stream.return_value = ifd_entry_
        return _IfdEntry_

    @pytest.fixture
    def _AsciiIfdEntry_(self, request, ifd_entry_):
        _AsciiIfdEntry_ = class_mock(request, "docx.image.tiff._AsciiIfdEntry")
        _AsciiIfdEntry_.from_stream.return_value = ifd_entry_
        return _AsciiIfdEntry_

    @pytest.fixture
    def _ShortIfdEntry_(self, request, ifd_entry_):
        _ShortIfdEntry_ = class_mock(request, "docx.image.tiff._ShortIfdEntry")
        _ShortIfdEntry_.from_stream.return_value = ifd_entry_
        return _ShortIfdEntry_

    @pytest.fixture
    def _LongIfdEntry_(self, request, ifd_entry_):
        _LongIfdEntry_ = class_mock(request, "docx.image.tiff._LongIfdEntry")
        _LongIfdEntry_.from_stream.return_value = ifd_entry_
        return _LongIfdEntry_

    @pytest.fixture
    def _RationalIfdEntry_(self, request, ifd_entry_):
        _RationalIfdEntry_ = class_mock(request, "docx.image.tiff._RationalIfdEntry")
        _RationalIfdEntry_.from_stream.return_value = ifd_entry_
        return _RationalIfdEntry_

    @pytest.fixture
    def offset_(self, request):
        return instance_mock(request, int)


class Describe_IfdEntry:
    def it_can_construct_from_a_stream_and_offset(
        self, _parse_value_, _IfdEntry__init_, value_
    ):
        bytes_ = b"\x00\x01\x66\x66\x00\x00\x00\x02\x00\x00\x00\x03"
        stream_rdr = StreamReader(io.BytesIO(bytes_), BIG_ENDIAN)
        offset, tag_code, value_count, value_offset = 0, 1, 2, 3
        _parse_value_.return_value = value_

        ifd_entry = _IfdEntry.from_stream(stream_rdr, offset)

        _parse_value_.assert_called_once_with(
            stream_rdr, offset, value_count, value_offset
        )
        _IfdEntry__init_.assert_called_once_with(ANY, tag_code, value_)
        assert isinstance(ifd_entry, _IfdEntry)

    def it_provides_read_only_access_to_the_directory_entry(self):
        tag_code, value = 1, 2
        ifd_entry = _IfdEntry(tag_code, value)
        assert (ifd_entry.tag, ifd_entry.value) == (tag_code, value)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def _IfdEntry__init_(self, request):
        return initializer_mock(request, _IfdEntry)

    @pytest.fixture
    def _parse_value_(self, request):
        return method_mock(request, _IfdEntry, "_parse_value", autospec=False)

    @pytest.fixture
    def value_(self, request):
        return loose_mock(request)


class Describe_AsciiIfdEntry:
    def it_can_parse_an_ascii_string_IFD_entry(self):
        bytes_ = b"foobar\x00"
        stream_rdr = StreamReader(io.BytesIO(bytes_), BIG_ENDIAN)
        val = _AsciiIfdEntry._parse_value(stream_rdr, None, 7, 0)
        assert val == "foobar"


class Describe_ShortIfdEntry:
    def it_can_parse_a_short_int_IFD_entry(self):
        bytes_ = b"foobaroo\x00\x2A"
        stream_rdr = StreamReader(io.BytesIO(bytes_), BIG_ENDIAN)
        val = _ShortIfdEntry._parse_value(stream_rdr, 0, 1, None)
        assert val == 42


class Describe_LongIfdEntry:
    def it_can_parse_a_long_int_IFD_entry(self):
        bytes_ = b"foobaroo\x00\x00\x00\x2A"
        stream_rdr = StreamReader(io.BytesIO(bytes_), BIG_ENDIAN)
        val = _LongIfdEntry._parse_value(stream_rdr, 0, 1, None)
        assert val == 42


class Describe_RationalIfdEntry:
    def it_can_parse_a_rational_IFD_entry(self):
        bytes_ = b"\x00\x00\x00\x2A\x00\x00\x00\x54"
        stream_rdr = StreamReader(io.BytesIO(bytes_), BIG_ENDIAN)
        val = _RationalIfdEntry._parse_value(stream_rdr, None, 1, 0)
        assert val == 0.5
