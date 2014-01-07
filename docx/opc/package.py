# encoding: utf-8

"""
The :mod:`pptx.packaging` module coheres around the concerns of reading and
writing presentations to and from a .pptx file.
"""

from __future__ import absolute_import, print_function, unicode_literals

from .compat import cls_method_fn
from .constants import RELATIONSHIP_TYPE as RT
from .oxml import CT_Relationships, nsmap, serialize_part_xml
from .packuri import PACKAGE_URI, PackURI
from .pkgreader import PackageReader
from .pkgwriter import PackageWriter
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
    def main_document(self):
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
        # self._notify_before_marshal()
        for part in self.parts:
            part.before_marshal()
        PackageWriter.write(pkg_file, self.rels, self.parts)


class Part(object):
    """
    Base class for package parts. Provides common properties and methods, but
    intended to be subclassed in client code to implement specific part
    behaviors.
    """
    def __init__(
            self, partname, content_type, blob=None, element=None,
            package=None):
        super(Part, self).__init__()
        self._partname = partname
        self._content_type = content_type
        self._blob = blob
        self._element = element
        self._package = package

    # load/save interface to OpcPackage ------------------------------

    def after_unmarshal(self):
        """
        Entry point for post-unmarshaling processing, for example to parse
        the part XML. May be overridden by subclasses without forwarding call
        to super.
        """
        # don't place any code here, just catch call if not overridden by
        # subclass
        pass

    def before_marshal(self):
        """
        Entry point for pre-serialization processing, for example to finalize
        part naming if necessary. May be overridden by subclasses without
        forwarding call to super.
        """
        # don't place any code here, just catch call if not overridden by
        # subclass
        pass

    @property
    def blob(self):
        """
        Contents of this package part as a sequence of bytes. May be text or
        binary. Intended to be overridden by subclasses. Default behavior is
        to return load blob.
        """
        if self._element is not None:
            return serialize_part_xml(self._element)
        return self._blob

    @property
    def content_type(self):
        """
        Content type of this part.
        """
        return self._content_type

    @classmethod
    def load(cls, partname, content_type, blob, package):
        return cls(
            partname, content_type, blob=blob, element=None, package=package
        )

    def load_rel(self, reltype, target, rId, is_external=False):
        """
        Return newly added |_Relationship| instance of *reltype* between this
        part and *target* with key *rId*. Target mode is set to
        ``RTM.EXTERNAL`` if *is_external* is |True|. Intended for use during
        load from a serialized package, where the rId is well known. Other
        methods exist for adding a new relationship to a part when
        manipulating a part.
        """
        return self.rels.add_relationship(reltype, target, rId, is_external)

    @property
    def partname(self):
        """
        |PackURI| instance holding partname of this part, e.g.
        '/ppt/slides/slide1.xml'
        """
        return self._partname

    @partname.setter
    def partname(self, partname):
        if not isinstance(partname, PackURI):
            tmpl = "partname must be instance of PackURI, got '%s'"
            raise TypeError(tmpl % type(partname).__name__)
        self._partname = partname

    # relationship management interface for child objects ------------

    def drop_rel(self, rId):
        """
        Remove the relationship identified by *rId* if its reference count
        is less than 2. Relationships with a reference count of 0 are
        implicit relationships.
        """
        if self._rel_ref_count(rId) < 2:
            del self.rels[rId]

    def part_related_by(self, reltype):
        """
        Return part to which this part has a relationship of *reltype*.
        Raises |KeyError| if no such relationship is found and |ValueError|
        if more than one such relationship is found. Provides ability to
        resolve implicitly related part, such as Slide -> SlideLayout.
        """
        return self.rels.part_with_reltype(reltype)

    def relate_to(self, target, reltype, is_external=False):
        """
        Return rId key of relationship of *reltype* to *target*, from an
        existing relationship if there is one, otherwise a newly created one.
        """
        if is_external:
            return self.rels.get_or_add_ext_rel(reltype, target)
        else:
            rel = self.rels.get_or_add(reltype, target)
            return rel.rId

    @property
    def related_parts(self):
        """
        Dictionary mapping related parts by rId, so child objects can resolve
        explicit relationships present in the part XML, e.g. sldIdLst to a
        specific |Slide| instance.
        """
        return self.rels.related_parts

    @lazyproperty
    def rels(self):
        """
        |Relationships| instance holding the relationships for this part.
        """
        return Relationships(self._partname.baseURI)

    def target_ref(self, rId):
        """
        Return URL contained in target ref of relationship identified by
        *rId*.
        """
        rel = self.rels[rId]
        return rel.target_ref

    def _rel_ref_count(self, rId):
        """
        Return the count of references in this part's XML to the relationship
        identified by *rId*.
        """
        assert self._element is not None
        rIds = self._element.xpath('//@r:id', namespaces=nsmap)
        return len([_rId for _rId in rIds if _rId == rId])

    # ----------------------------------------------------------------

    @property
    def package(self):
        """
        |OpcPackage| instance this part belongs to.
        """
        return self._package


class PartFactory(object):
    """
    Provides a way for client code to specify a subclass of |Part| to be
    constructed by |Unmarshaller| based on its content type and/or a custom
    callable. Setting ``PartFactory.part_class_selector`` to a callable
    object will cause that object to be called with the parameters
    ``content_type, reltype``, once for each part in the package. If the
    callable returns an object, it is used as the class for that part. If it
    returns |None|, part class selection falls back to the content type map
    defined in ``PartFactory.part_type_for``. If no class is returned from
    either of these, the class contained in ``PartFactory.default_part_type``
    is used to construct the part, which is by default ``opc.package.Part``.
    """
    part_class_selector = None
    part_type_for = {}
    default_part_type = Part

    def __new__(cls, partname, content_type, reltype, blob, package):
        PartClass = None
        if cls.part_class_selector is not None:
            part_class_selector = cls_method_fn(cls, 'part_class_selector')
            PartClass = part_class_selector(content_type, reltype)
        if PartClass is None:
            PartClass = cls._part_cls_for(content_type)
        return PartClass.load(partname, content_type, blob, package)

    @classmethod
    def _part_cls_for(cls, content_type):
        """
        Return the custom part class registered for *content_type*, or the
        default part class if no custom class is registered for
        *content_type*.
        """
        if content_type in cls.part_type_for:
            return cls.part_type_for[content_type]
        return cls.default_part_type


class Relationships(dict):
    """
    Collection object for |_Relationship| instances, having list semantics.
    """
    def __init__(self, baseURI):
        super(Relationships, self).__init__()
        self._baseURI = baseURI
        self._target_parts_by_rId = {}

    def add_relationship(self, reltype, target, rId, is_external=False):
        """
        Return a newly added |_Relationship| instance.
        """
        rel = _Relationship(rId, reltype, target, self._baseURI, is_external)
        self[rId] = rel
        if not is_external:
            self._target_parts_by_rId[rId] = target
        return rel

    def get_or_add(self, reltype, target_part):
        """
        Return relationship of *reltype* to *target_part*, newly added if not
        already present in collection.
        """
        rel = self._get_matching(reltype, target_part)
        if rel is None:
            rId = self._next_rId
            rel = self.add_relationship(reltype, target_part, rId)
        return rel

    def get_or_add_ext_rel(self, reltype, target_ref):
        """
        Return rId of external relationship of *reltype* to *target_ref*,
        newly added if not already present in collection.
        """
        rel = self._get_matching(reltype, target_ref, is_external=True)
        if rel is None:
            rId = self._next_rId
            rel = self.add_relationship(
                reltype, target_ref, rId, is_external=True
            )
        return rel.rId

    def part_with_reltype(self, reltype):
        """
        Return target part of rel with matching *reltype*, raising |KeyError|
        if not found and |ValueError| if more than one matching relationship
        is found.
        """
        rel = self._get_rel_of_type(reltype)
        return rel.target_part

    @property
    def related_parts(self):
        """
        dict mapping rIds to target parts for all the internal relationships
        in the collection.
        """
        return self._target_parts_by_rId

    @property
    def xml(self):
        """
        Serialize this relationship collection into XML suitable for storage
        as a .rels file in an OPC package.
        """
        rels_elm = CT_Relationships.new()
        for rel in self.values():
            rels_elm.add_rel(
                rel.rId, rel.reltype, rel.target_ref, rel.is_external
            )
        return rels_elm.xml

    def _get_matching(self, reltype, target, is_external=False):
        """
        Return relationship of matching *reltype*, *target*, and
        *is_external* from collection, or None if not found.
        """
        def matches(rel, reltype, target, is_external):
            if rel.reltype != reltype:
                return False
            if rel.is_external != is_external:
                return False
            rel_target = rel.target_ref if rel.is_external else rel.target_part
            if rel_target != target:
                return False
            return True

        for rel in self.values():
            if matches(rel, reltype, target, is_external):
                return rel
        return None

    def _get_rel_of_type(self, reltype):
        """
        Return single relationship of type *reltype* from the collection.
        Raises |KeyError| if no matching relationship is found. Raises
        |ValueError| if more than one matching relationship is found.
        """
        matching = [rel for rel in self.values() if rel.reltype == reltype]
        if len(matching) == 0:
            tmpl = "no relationship of type '%s' in collection"
            raise KeyError(tmpl % reltype)
        if len(matching) > 1:
            tmpl = "multiple relationships of type '%s' in collection"
            raise ValueError(tmpl % reltype)
        return matching[0]

    @property
    def _next_rId(self):
        """
        Next available rId in collection, starting from 'rId1' and making use
        of any gaps in numbering, e.g. 'rId2' for rIds ['rId1', 'rId3'].
        """
        for n in range(1, len(self)+2):
            rId_candidate = 'rId%d' % n  # like 'rId19'
            if rId_candidate not in self:
                return rId_candidate


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


class _Relationship(object):
    """
    Value object for relationship to part.
    """
    def __init__(self, rId, reltype, target, baseURI, external=False):
        super(_Relationship, self).__init__()
        self._rId = rId
        self._reltype = reltype
        self._target = target
        self._baseURI = baseURI
        self._is_external = bool(external)

    @property
    def is_external(self):
        return self._is_external

    @property
    def reltype(self):
        return self._reltype

    @property
    def rId(self):
        return self._rId

    @property
    def target_part(self):
        if self._is_external:
            raise ValueError("target_part property on _Relationship is undef"
                             "ined when target mode is External")
        return self._target

    @property
    def target_ref(self):
        if self._is_external:
            return self._target
        else:
            return self._target.partname.relative_ref(self._baseURI)
