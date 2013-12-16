# encoding: utf-8

"""
Provides a low-level, write-only API to a serialized Open Packaging
Convention (OPC) package, essentially an implementation of OpcPackage.save()
"""

from __future__ import absolute_import

from .constants import CONTENT_TYPE as CT
from .oxml import CT_Types, serialize_part_xml
from .packuri import CONTENT_TYPES_URI, PACKAGE_URI
from .phys_pkg import PhysPkgWriter
from .spec import default_content_types


class PackageWriter(object):
    """
    Writes a zip-format OPC package to *pkg_file*, where *pkg_file* can be
    either a path to a zip file (a string) or a file-like object. Its single
    API method, :meth:`write`, is static, so this class is not intended to
    be instantiated.
    """
    @staticmethod
    def write(pkg_file, pkg_rels, parts):
        """
        Write a physical package (.pptx file) to *pkg_file* containing
        *pkg_rels* and *parts* and a content types stream based on the
        content types of the parts.
        """
        phys_writer = PhysPkgWriter(pkg_file)
        PackageWriter._write_content_types_stream(phys_writer, parts)
        PackageWriter._write_pkg_rels(phys_writer, pkg_rels)
        PackageWriter._write_parts(phys_writer, parts)
        phys_writer.close()

    @staticmethod
    def _write_content_types_stream(phys_writer, parts):
        """
        Write ``[Content_Types].xml`` part to the physical package with an
        appropriate content type lookup target for each part in *parts*.
        """
        phys_writer.write(CONTENT_TYPES_URI, _ContentTypesItem.xml_for(parts))

    @staticmethod
    def _write_parts(phys_writer, parts):
        """
        Write the blob of each part in *parts* to the package, along with a
        rels item for its relationships if and only if it has any.
        """
        for part in parts:
            phys_writer.write(part.partname, part.blob)
            if len(part._rels):
                phys_writer.write(part.partname.rels_uri, part._rels.xml)

    @staticmethod
    def _write_pkg_rels(phys_writer, pkg_rels):
        """
        Write the XML rels item for *pkg_rels* ('/_rels/.rels') to the
        package.
        """
        phys_writer.write(PACKAGE_URI.rels_uri, pkg_rels.xml)


class _ContentTypesItem(object):
    """
    Service class that composes a content types item ([Content_Types].xml)
    based on a list of parts. Not meant to be instantiated, its single
    interface method is xml_for(), e.g. ``_ContentTypesItem.xml_for(parts)``.
    """
    @staticmethod
    def xml_for(parts):
        """
        Return content types XML mapping each part in *parts* to the
        appropriate content type and suitable for storage as
        ``[Content_Types].xml`` in an OPC package.
        """
        defaults = dict((('.rels', CT.OPC_RELATIONSHIPS), ('.xml', CT.XML)))
        overrides = dict()
        for part in parts:
            _ContentTypesItem._add_content_type(
                defaults, overrides, part.partname, part.content_type
            )
        return _ContentTypesItem._xml(defaults, overrides)

    @staticmethod
    def _add_content_type(defaults, overrides, partname, content_type):
        """
        Add a content type for the part with *partname* and *content_type*,
        using a default or override as appropriate.
        """
        ext = partname.ext
        if (ext, content_type) in default_content_types:
            defaults[ext] = content_type
        else:
            overrides[partname] = content_type

    @staticmethod
    def _xml(defaults, overrides):
        """
        XML form of this content types item, suitable for storage as
        ``[Content_Types].xml`` in an OPC package. Although the sequence of
        elements is not strictly significant, as an aid to testing and
        readability Default elements are sorted by extension and Override
        elements are sorted by partname.
        """
        _types_elm = CT_Types.new()
        for ext in sorted(defaults.keys()):
            _types_elm.add_default(ext, defaults[ext])
        for partname in sorted(overrides.keys()):
            _types_elm.add_override(partname, overrides[partname])
        return serialize_part_xml(_types_elm)
