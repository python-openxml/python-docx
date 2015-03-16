# encoding: utf-8

"""
Test suite for the docx.parts.settings module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.parts.settings import SettingsPart
from docx.settings import Settings

from ..unitutil.cxml import element
from ..unitutil.mock import class_mock, instance_mock


class DescribeSettingsPart(object):

    def it_provides_access_to_its_settings(self, settings_fixture):
        settings_part, Settings_, settings_ = settings_fixture
        settings = settings_part.settings
        Settings_.assert_called_once_with(settings_part.element)
        assert settings is settings_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def settings_fixture(self, Settings_, settings_):
        settings_elm = element('w:settings')
        settings_part = SettingsPart(None, None, settings_elm, None)
        return settings_part, Settings_, settings_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def Settings_(self, request, settings_):
        return class_mock(
            request, 'docx.parts.settings.Settings', return_value=settings_
        )

    @pytest.fixture
    def settings_(self, request):
        return instance_mock(request, Settings)
