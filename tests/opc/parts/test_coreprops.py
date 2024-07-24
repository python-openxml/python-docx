"""Unit test suite for the docx.opc.parts.coreprops module."""

from __future__ import annotations

import datetime as dt

import pytest

from docx.opc.coreprops import CoreProperties
from docx.opc.package import OpcPackage
from docx.opc.packuri import PackURI
from docx.opc.parts.coreprops import CorePropertiesPart

from ...unitutil.cxml import element
from ...unitutil.mock import FixtureRequest, Mock, class_mock, instance_mock


class DescribeCorePropertiesPart:
    """Unit-test suite for `docx.opc.parts.coreprops.CorePropertiesPart` objects."""

    def it_provides_access_to_its_core_props_object(self, CoreProperties_: Mock, package_: Mock):
        core_properties_part = CorePropertiesPart(
            PackURI("/part/name"), "content/type", element("cp:coreProperties"), package_
        )

        core_properties = core_properties_part.core_properties

        CoreProperties_.assert_called_once_with(core_properties_part.element)
        assert isinstance(core_properties, CoreProperties)

    def it_can_create_a_default_core_properties_part(self, package_: Mock):
        core_properties_part = CorePropertiesPart.default(package_)

        assert isinstance(core_properties_part, CorePropertiesPart)
        # --
        core_properties = core_properties_part.core_properties
        assert core_properties.title == "Word Document"
        assert core_properties.last_modified_by == "python-docx"
        assert core_properties.revision == 1
        assert core_properties.modified is not None
        delta = dt.datetime.now(dt.timezone.utc) - core_properties.modified
        max_expected_delta = dt.timedelta(seconds=2)
        assert delta < max_expected_delta

    # fixtures ---------------------------------------------

    @pytest.fixture
    def CoreProperties_(self, request: FixtureRequest):
        return class_mock(request, "docx.opc.parts.coreprops.CoreProperties")

    @pytest.fixture
    def package_(self, request: FixtureRequest):
        return instance_mock(request, OpcPackage)
