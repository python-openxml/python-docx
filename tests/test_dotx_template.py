"""Tests for Issue #1532: .dotx template support."""

import os

import pytest

from docx import Document
from docx.package import Package
from docx.parts.document import DocumentPart


class DescribeDotxTemplate:
    """Unit-test suite for .dotx file support."""

    def it_can_load_a_dotx_template_file(self):
        """Test loading a real .dotx file."""
        template_path = "test_dotx_real.dotx"

        if not os.path.exists(template_path):
            pytest.skip(f"Template file {template_path} not found")

        # It should load the file successfully
        doc = Document(template_path)
        assert doc is not None
        assert hasattr(doc, "paragraphs")

    def it_creates_document_part_for_dotx_files(self):
        """Test that .dotx files create DocumentPart, not generic Part."""
        template_path = "test_dotx_real.dotx"

        if not os.path.exists(template_path):
            pytest.skip(f"Template file {template_path} not found")

        pkg = Package.open(template_path)
        # It should create a DocumentPart, not a generic Part
        assert isinstance(pkg.main_document_part, DocumentPart)