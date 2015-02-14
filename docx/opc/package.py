# encoding: utf-8

"""
The :mod:`pptx.packaging` module coheres around the concerns of reading and
writing presentations to and from a .pptx file.
"""

from __future__ import absolute_import, print_function, unicode_literals

from .constants import RELATIONSHIP_TYPE as RT
from .packuri import PACKAGE_URI
from .part import PartFactory
from .parts.coreprops import CorePropertiesPart
from .pkgreader import PackageReader
from .pkgwriter import PackageWriter
from .rel import Relationships
from .shared import lazyproperty


class OpcPackage(object):
    """
    Main API class for |python-opc|. A new instance is constructed by calling
    the :meth:`open` class method with a path to a package file or file-like
    object containing one.
    """
    def __init__(self):
        super(OpcPackage, self).__init__()

    def after_unmarshal(self):
        """
        Entry point for any post-unmarshaling processing. May be overridden
        by subclasses without forwarding call to super.
        """
        # don't place any code here, just catch call if not overridden by
        # subclass
        pass

    @property
    def core_properties(self):
        """
        |CoreProperties| object providing read/write access to the Dublin
        Core properties for this document.
        """
        return self._core_properties_part.core_properties

    def iter_rels(self):
        """
        Generate exactly one reference to each relationship in the package by
        performing a depth-first traversal of the rels graph.
        """
        def walk_rels(source, visited=None):
            visited = [] if visited is None else visited
            for rel in source.rels.values():
                yield rel
                if rel.is_external:
                    continue
                part = rel.target_part
                if part in visited:
                    continue
                visited.append(part)
                new_source = part
                for rel in walk_rels(new_source, visited):
                    yield rel

        for rel in walk_rels(self):
            yield rel

    def iter_parts(self):
        """
        Generate exactly one reference to each of the parts in the package by
        performing a depth-first traversal of the rels graph.
        """
        def walk_parts(source, visited=list()):
            for rel in source.rels.values():
                if rel.is_external:
                    continue
                part = rel.target_part
                if part in visited:
                    continue
                visited.append(part)
                yield part
                new_source = part
                for part in walk_parts(new_source, visited):
                    yield part

        for part in walk_parts(self):
            yield part

    def load_rel(self, reltype, target, rId, is_external=False):
        """
        Return newly added |_Relationship| instance of *reltype* between this
        part and *target* with key *rId*. Target mode is set to
        ``RTM.EXTERNAL`` if *is_external* is |True|. Intended for use during
        load from a serialized package, where the rId is well known. Other
        methods exist for adding a new relationship to the package during
        processing.
        """
        return self.rels.add_relationship(reltype, target, rId, is_external)

    @property
    def main_document_part(self):
        """
        Return a reference to the main document part for this package.
        Examples include a document part for a WordprocessingML package, a
        presentation part for a PresentationML package, or a workbook part
        for a SpreadsheetML package.
        """
        return self.part_related_by(RT.OFFICE_DOCUMENT)

    @classmethod
    def open(cls, pkg_file):
        """
        Return an |OpcPackage| instance loaded with the contents of
        *pkg_file*.
        """
        pkg_reader = PackageReader.from_file(pkg_file)
        package = cls()
        Unmarshaller.unmarshal(pkg_reader, package, PartFactory)
        return package

    def part_related_by(self, reltype):
        """
        Return part to which this package has a relationship of *reltype*.
        Raises |KeyError| if no such relationship is found and |ValueError|
        if more than one such relationship is found.
        """
        return self.rels.part_with_reltype(reltype)

    @property
    def parts(self):
        """
        Return a list containing a reference to each of the parts in this
        package.
        """
        return [part for part in self.iter_parts()]

    def relate_to(self, part, reltype):
        """
        Return rId key of relationship to *part*, from the existing
        relationship if there is one, otherwise a newly created one.
        """
        rel = self.rels.get_or_add(reltype, part)
        return rel.rId

    @lazyproperty
    def rels(self):
        """
        Return a reference to the |Relationships| instance holding the
        collection of relationships for this package.
        """
        return Relationships(PACKAGE_URI.baseURI)

    def save(self, pkg_file):
        """
        Save this package to *pkg_file*, where *file* can be either a path to
        a file (a string) or a file-like object.
        """
        for part in self.parts:
            part.before_marshal()
        PackageWriter.write(pkg_file, self.rels, self.parts)

    @property
    def _core_properties_part(self):
        """
        |CorePropertiesPart| object related to this package. Creates
        a default core properties part if one is not present (not common).
        """
        try:
            return self.part_related_by(RT.CORE_PROPERTIES)
        except KeyError:
            core_properties_part = CorePropertiesPart.default(self)
            self.relate_to(core_properties_part, RT.CORE_PROPERTIES)
            return core_properties_part


class Unmarshaller(object):
    """
    Hosts static methods for unmarshalling a package from a |PackageReader|
    instance.
    """
    @staticmethod
    def unmarshal(pkg_reader, package, part_factory):
        """
        Construct graph of parts and realized relationships based on the
        contents of *pkg_reader*, delegating construction of each part to
        *part_factory*. Package relationships are added to *pkg*.
        """
        parts = Unmarshaller._unmarshal_parts(
            pkg_reader, package, part_factory
        )
        Unmarshaller._unmarshal_relationships(pkg_reader, package, parts)
        for part in parts.values():
            part.after_unmarshal()
        package.after_unmarshal()

    @staticmethod
    def _unmarshal_parts(pkg_reader, package, part_factory):
        """
        Return a dictionary of |Part| instances unmarshalled from
        *pkg_reader*, keyed by partname. Side-effect is that each part in
        *pkg_reader* is constructed using *part_factory*.
        """
        parts = {}
        for partname, content_type, reltype, blob in pkg_reader.iter_sparts():
            parts[partname] = part_factory(
                partname, content_type, reltype, blob, package
            )
        return parts

    @staticmethod
    def _unmarshal_relationships(pkg_reader, package, parts):
        """
        Add a relationship to the source object corresponding to each of the
        relationships in *pkg_reader* with its target_part set to the actual
        target part in *parts*.
        """
        for source_uri, srel in pkg_reader.iter_srels():
            source = package if source_uri == '/' else parts[source_uri]
            target = (srel.target_ref if srel.is_external
                      else parts[srel.target_partname])
            source.load_rel(srel.reltype, target, srel.rId, srel.is_external)
