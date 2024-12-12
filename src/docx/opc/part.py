# pyright: reportImportCycles=false

"""Open Packaging Convention (OPC) objects related to package parts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Type, cast

from docx.opc.oxml import serialize_part_xml
from docx.opc.packuri import PackURI
from docx.opc.rel import Relationships
from docx.opc.shared import cls_method_fn
from docx.oxml.parser import parse_xml
from docx.shared import lazyproperty

if TYPE_CHECKING:
    from docx.oxml.xmlchemy import BaseOxmlElement
    from docx.package import Package


class Part:
    """Base class for package parts.

    Provides common properties and methods, but intended to be subclassed in client code
    to implement specific part behaviors.
    """

    def __init__(
        self,
        partname: PackURI,
        content_type: str,
        blob: bytes | None = None,
        package: Package | None = None,
    ):
        super(Part, self).__init__()
        self._partname = partname
        self._content_type = content_type
        self._blob = blob
        self._package = package

    def after_unmarshal(self):
        """Entry point for post-unmarshaling processing, for example to parse the part
        XML.

        May be overridden by subclasses without forwarding call to super.
        """
        # don't place any code here, just catch call if not overridden by
        # subclass
        pass

    def before_marshal(self):
        """Entry point for pre-serialization processing, for example to finalize part
        naming if necessary.

        May be overridden by subclasses without forwarding call to super.
        """
        # don't place any code here, just catch call if not overridden by
        # subclass
        pass

    @property
    def blob(self) -> bytes:
        """Contents of this package part as a sequence of bytes.

        May be text or binary. Intended to be overridden by subclasses. Default behavior
        is to return load blob.
        """
        return self._blob or b""

    @property
    def content_type(self):
        """Content type of this part."""
        return self._content_type

    def drop_rel(self, rId: str):
        """Remove the relationship identified by `rId` if its reference count is less
        than 2.

        Relationships with a reference count of 0 are implicit relationships.
        """
        if self._rel_ref_count(rId) < 2:
            del self.rels[rId]

    @classmethod
    def load(cls, partname: PackURI, content_type: str, blob: bytes, package: Package):
        return cls(partname, content_type, blob, package)

    def load_rel(self, reltype: str, target: Part | str, rId: str, is_external: bool = False):
        """Return newly added |_Relationship| instance of `reltype`.

        The new relationship relates the `target` part to this part with key `rId`.

        Target mode is set to ``RTM.EXTERNAL`` if `is_external` is |True|. Intended for
        use during load from a serialized package, where the rId is well-known. Other
        methods exist for adding a new relationship to a part when manipulating a part.
        """
        return self.rels.add_relationship(reltype, target, rId, is_external)

    @property
    def package(self):
        """|OpcPackage| instance this part belongs to."""
        return self._package

    @property
    def partname(self):
        """|PackURI| instance holding partname of this part, e.g.
        '/ppt/slides/slide1.xml'."""
        return self._partname

    @partname.setter
    def partname(self, partname: str):
        if not isinstance(partname, PackURI):
            tmpl = "partname must be instance of PackURI, got '%s'"
            raise TypeError(tmpl % type(partname).__name__)
        self._partname = partname

    def part_related_by(self, reltype: str) -> Part:
        """Return part to which this part has a relationship of `reltype`.

        Raises |KeyError| if no such relationship is found and |ValueError| if more than
        one such relationship is found. Provides ability to resolve implicitly related
        part, such as Slide -> SlideLayout.
        """
        return self.rels.part_with_reltype(reltype)

    def relate_to(self, target: Part | str, reltype: str, is_external: bool = False) -> str:
        """Return rId key of relationship of `reltype` to `target`.

        The returned `rId` is from an existing relationship if there is one, otherwise a
        new relationship is created.
        """
        if is_external:
            return self.rels.get_or_add_ext_rel(reltype, cast(str, target))
        else:
            rel = self.rels.get_or_add(reltype, cast(Part, target))
            return rel.rId

    @property
    def related_parts(self):
        """Dictionary mapping related parts by rId, so child objects can resolve
        explicit relationships present in the part XML, e.g. sldIdLst to a specific
        |Slide| instance."""
        return self.rels.related_parts

    @lazyproperty
    def rels(self):
        """|Relationships| instance holding the relationships for this part."""
        # -- prevent breakage in `python-docx-template` by retaining legacy `._rels` attribute --
        self._rels = Relationships(self._partname.baseURI)
        return self._rels

    def target_ref(self, rId: str) -> str:
        """Return URL contained in target ref of relationship identified by `rId`."""
        rel = self.rels[rId]
        return rel.target_ref

    def _rel_ref_count(self, rId: str) -> int:
        """Return the count of references in this part to the relationship identified by `rId`.

        Only an XML part can contain references, so this is 0 for `Part`.
        """
        return 0


class PartFactory:
    """Provides a way for client code to specify a subclass of |Part| to be constructed
    by |Unmarshaller| based on its content type and/or a custom callable.

    Setting ``PartFactory.part_class_selector`` to a callable object will cause that
    object to be called with the parameters ``content_type, reltype``, once for each
    part in the package. If the callable returns an object, it is used as the class for
    that part. If it returns |None|, part class selection falls back to the content type
    map defined in ``PartFactory.part_type_for``. If no class is returned from either of
    these, the class contained in ``PartFactory.default_part_type`` is used to construct
    the part, which is by default ``opc.package.Part``.
    """

    part_class_selector: Callable[[str, str], Type[Part] | None] | None
    part_type_for: dict[str, Type[Part]] = {}
    default_part_type = Part

    def __new__(
        cls,
        partname: PackURI,
        content_type: str,
        reltype: str,
        blob: bytes,
        package: Package,
    ):
        PartClass: Type[Part] | None = None
        if cls.part_class_selector is not None:
            part_class_selector = cls_method_fn(cls, "part_class_selector")
            PartClass = part_class_selector(content_type, reltype)
        if PartClass is None:
            PartClass = cls._part_cls_for(content_type)
        return PartClass.load(partname, content_type, blob, package)

    @classmethod
    def _part_cls_for(cls, content_type: str):
        """Return the custom part class registered for `content_type`, or the default
        part class if no custom class is registered for `content_type`."""
        if content_type in cls.part_type_for:
            return cls.part_type_for[content_type]
        return cls.default_part_type


class XmlPart(Part):
    """Base class for package parts containing an XML payload, which is most of them.

    Provides additional methods to the |Part| base class that take care of parsing and
    reserializing the XML payload and managing relationships to other parts.
    """

    def __init__(
        self, partname: PackURI, content_type: str, element: BaseOxmlElement, package: Package
    ):
        super(XmlPart, self).__init__(partname, content_type, package=package)
        self._element = element

    @property
    def blob(self):
        return serialize_part_xml(self._element)

    @property
    def element(self):
        """The root XML element of this XML part."""
        return self._element

    @classmethod
    def load(cls, partname: PackURI, content_type: str, blob: bytes, package: Package):
        element = parse_xml(blob)
        return cls(partname, content_type, element, package)

    @property
    def part(self):
        """Part of the parent protocol, "children" of the document will not know the
        part that contains them so must ask their parent object.

        That chain of delegation ends here for child objects.
        """
        return self

    def _rel_ref_count(self, rId: str) -> int:
        """Return the count of references in this part's XML to the relationship
        identified by `rId`."""
        rIds = cast("list[str]", self._element.xpath("//@r:id"))
        return len([_rId for _rId in rIds if _rId == rId])
