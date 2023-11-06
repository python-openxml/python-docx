"""Unit test suite for the docx.settings module."""

import pytest

from docx.settings import Settings

from .unitutil.cxml import element, xml


class DescribeSettings:
    def it_knows_when_the_document_has_distinct_odd_and_even_headers(
        self, odd_and_even_get_fixture
    ):
        settings_elm, expected_value = odd_and_even_get_fixture
        settings = Settings(settings_elm)

        odd_and_even_pages_header_footer = settings.odd_and_even_pages_header_footer

        assert odd_and_even_pages_header_footer is expected_value

    def it_can_change_whether_the_document_has_distinct_odd_and_even_headers(
        self, odd_and_even_set_fixture
    ):
        settings_elm, value, expected_xml = odd_and_even_set_fixture
        settings = Settings(settings_elm)

        settings.odd_and_even_pages_header_footer = value

        assert settings_elm.xml == expected_xml

    def it_knows_when_the_document_has_track_revisions(
        self, track_revisions_get_fixture
    ):
        settings_elm, expected_value = track_revisions_get_fixture
        settings = Settings(settings_elm)

        track_revisions = settings.track_revisions

        assert track_revisions is expected_value

    def it_can_change_whether_the_document_has_track_revisions(
        self, track_revisions_set_fixture
    ):
        settings_elm, value, expected_xml = track_revisions_set_fixture
        settings = Settings(settings_elm)

        settings.track_revisions = value

        assert settings_elm.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("w:settings", False),
            ("w:settings/w:evenAndOddHeaders", True),
            ("w:settings/w:evenAndOddHeaders{w:val=0}", False),
            ("w:settings/w:evenAndOddHeaders{w:val=1}", True),
            ("w:settings/w:evenAndOddHeaders{w:val=true}", True),
        ]
    )
    def odd_and_even_get_fixture(self, request):
        settings_cxml, expected_value = request.param
        settings_elm = element(settings_cxml)
        return settings_elm, expected_value

    @pytest.fixture(
        params=[
            ("w:settings", True, "w:settings/w:evenAndOddHeaders"),
            ("w:settings/w:evenAndOddHeaders", False, "w:settings"),
            (
                "w:settings/w:evenAndOddHeaders{w:val=1}",
                True,
                "w:settings/w:evenAndOddHeaders",
            ),
            ("w:settings/w:evenAndOddHeaders{w:val=off}", False, "w:settings"),
        ]
    )
    def odd_and_even_set_fixture(self, request):
        settings_cxml, value, expected_cxml = request.param
        settings_elm = element(settings_cxml)
        expected_xml = xml(expected_cxml)
        return settings_elm, value, expected_xml

    @pytest.fixture(
        params=[
            ("w:settings", False),
            ("w:settings/w:trackRevisions", True),
            ("w:settings/w:trackRevisions{w:val=0}", False),
            ("w:settings/w:trackRevisions{w:val=1}", True),
            ("w:settings/w:trackRevisions{w:val=true}", True),
        ]
    )
    def track_revisions_get_fixture(self, request):
        settings_cxml, expected_value = request.param
        settings_elm = element(settings_cxml)
        return settings_elm, expected_value

    @pytest.fixture(
        params=[
            ("w:settings", True, "w:settings/w:trackRevisions"),
            ("w:settings/w:trackRevisions", False, "w:settings"),
            (
                "w:settings/w:trackRevisions{w:val=1}",
                True,
                "w:settings/w:trackRevisions",
            ),
            ("w:settings/w:trackRevisions{w:val=off}", False, "w:settings"),
        ]
    )
    def track_revisions_set_fixture(self, request):
        settings_cxml, value, expected_cxml = request.param
        settings_elm = element(settings_cxml)
        expected_xml = xml(expected_cxml)
        return settings_elm, value, expected_xml
