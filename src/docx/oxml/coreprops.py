"""Custom element classes for core properties-related XML elements."""

import re
from datetime import datetime, timedelta
from typing import Any

from docx.oxml.ns import nsdecls, qn
from docx.oxml.parser import parse_xml
from docx.oxml.xmlchemy import BaseOxmlElement, ZeroOrOne


class CT_CoreProperties(BaseOxmlElement):
    """`<cp:coreProperties>` element, the root element of the Core Properties part.

    Stored as `/docProps/core.xml`. Implements many of the Dublin Core document metadata
    elements. String elements resolve to an empty string ("") if the element is not
    present in the XML. String elements are limited in length to 255 unicode characters.
    """

    category = ZeroOrOne("cp:category", successors=())
    contentStatus = ZeroOrOne("cp:contentStatus", successors=())
    created = ZeroOrOne("dcterms:created", successors=())
    creator = ZeroOrOne("dc:creator", successors=())
    description = ZeroOrOne("dc:description", successors=())
    identifier = ZeroOrOne("dc:identifier", successors=())
    keywords = ZeroOrOne("cp:keywords", successors=())
    language = ZeroOrOne("dc:language", successors=())
    lastModifiedBy = ZeroOrOne("cp:lastModifiedBy", successors=())
    lastPrinted = ZeroOrOne("cp:lastPrinted", successors=())
    modified = ZeroOrOne("dcterms:modified", successors=())
    revision = ZeroOrOne("cp:revision", successors=())
    subject = ZeroOrOne("dc:subject", successors=())
    title = ZeroOrOne("dc:title", successors=())
    version = ZeroOrOne("cp:version", successors=())

    _coreProperties_tmpl = "<cp:coreProperties %s/>\n" % nsdecls("cp", "dc", "dcterms")

    @classmethod
    def new(cls):
        """Return a new `<cp:coreProperties>` element."""
        xml = cls._coreProperties_tmpl
        coreProperties = parse_xml(xml)
        return coreProperties

    @property
    def author_text(self):
        """The text in the `dc:creator` child element."""
        return self._text_of_element("creator")

    @author_text.setter
    def author_text(self, value: str):
        self._set_element_text("creator", value)

    @property
    def category_text(self) -> str:
        return self._text_of_element("category")

    @category_text.setter
    def category_text(self, value: str):
        self._set_element_text("category", value)

    @property
    def comments_text(self) -> str:
        return self._text_of_element("description")

    @comments_text.setter
    def comments_text(self, value: str):
        self._set_element_text("description", value)

    @property
    def contentStatus_text(self):
        return self._text_of_element("contentStatus")

    @contentStatus_text.setter
    def contentStatus_text(self, value: str):
        self._set_element_text("contentStatus", value)

    @property
    def created_datetime(self):
        return self._datetime_of_element("created")

    @created_datetime.setter
    def created_datetime(self, value):
        self._set_element_datetime("created", value)

    @property
    def identifier_text(self):
        return self._text_of_element("identifier")

    @identifier_text.setter
    def identifier_text(self, value):
        self._set_element_text("identifier", value)

    @property
    def keywords_text(self):
        return self._text_of_element("keywords")

    @keywords_text.setter
    def keywords_text(self, value):
        self._set_element_text("keywords", value)

    @property
    def language_text(self):
        return self._text_of_element("language")

    @language_text.setter
    def language_text(self, value):
        self._set_element_text("language", value)

    @property
    def lastModifiedBy_text(self):
        return self._text_of_element("lastModifiedBy")

    @lastModifiedBy_text.setter
    def lastModifiedBy_text(self, value):
        self._set_element_text("lastModifiedBy", value)

    @property
    def lastPrinted_datetime(self):
        return self._datetime_of_element("lastPrinted")

    @lastPrinted_datetime.setter
    def lastPrinted_datetime(self, value):
        self._set_element_datetime("lastPrinted", value)

    @property
    def modified_datetime(self):
        return self._datetime_of_element("modified")

    @modified_datetime.setter
    def modified_datetime(self, value):
        self._set_element_datetime("modified", value)

    @property
    def revision_number(self):
        """Integer value of revision property."""
        revision = self.revision
        if revision is None:
            return 0
        revision_str = revision.text
        try:
            revision = int(revision_str)
        except ValueError:
            # non-integer revision strings also resolve to 0
            revision = 0
        # as do negative integers
        if revision < 0:
            revision = 0
        return revision

    @revision_number.setter
    def revision_number(self, value):
        """Set revision property to string value of integer `value`."""
        if not isinstance(value, int) or value < 1:
            tmpl = "revision property requires positive int, got '%s'"
            raise ValueError(tmpl % value)
        revision = self.get_or_add_revision()
        revision.text = str(value)

    @property
    def subject_text(self):
        return self._text_of_element("subject")

    @subject_text.setter
    def subject_text(self, value):
        self._set_element_text("subject", value)

    @property
    def title_text(self):
        return self._text_of_element("title")

    @title_text.setter
    def title_text(self, value):
        self._set_element_text("title", value)

    @property
    def version_text(self):
        return self._text_of_element("version")

    @version_text.setter
    def version_text(self, value):
        self._set_element_text("version", value)

    def _datetime_of_element(self, property_name):
        element = getattr(self, property_name)
        if element is None:
            return None
        datetime_str = element.text
        try:
            return self._parse_W3CDTF_to_datetime(datetime_str)
        except ValueError:
            # invalid datetime strings are ignored
            return None

    def _get_or_add(self, prop_name):
        """Return element returned by "get_or_add_" method for `prop_name`."""
        get_or_add_method_name = "get_or_add_%s" % prop_name
        get_or_add_method = getattr(self, get_or_add_method_name)
        element = get_or_add_method()
        return element

    @classmethod
    def _offset_dt(cls, dt, offset_str):
        """A |datetime| instance offset from `dt` by timezone offset in `offset_str`.

        `offset_str` is like `"-07:00"`.
        """
        match = cls._offset_pattern.match(offset_str)
        if match is None:
            raise ValueError("'%s' is not a valid offset string" % offset_str)
        sign, hours_str, minutes_str = match.groups()
        sign_factor = -1 if sign == "+" else 1
        hours = int(hours_str) * sign_factor
        minutes = int(minutes_str) * sign_factor
        td = timedelta(hours=hours, minutes=minutes)
        return dt + td

    _offset_pattern = re.compile(r"([+-])(\d\d):(\d\d)")

    @classmethod
    def _parse_W3CDTF_to_datetime(cls, w3cdtf_str):
        # valid W3CDTF date cases:
        # yyyy e.g. "2003"
        # yyyy-mm e.g. "2003-12"
        # yyyy-mm-dd e.g. "2003-12-31"
        # UTC timezone e.g. "2003-12-31T10:14:55Z"
        # numeric timezone e.g. "2003-12-31T10:14:55-08:00"
        templates = (
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d",
            "%Y-%m",
            "%Y",
        )
        # strptime isn't smart enough to parse literal timezone offsets like
        # "-07:30", so we have to do it ourselves
        parseable_part = w3cdtf_str[:19]
        offset_str = w3cdtf_str[19:]
        dt = None
        for tmpl in templates:
            try:
                dt = datetime.strptime(parseable_part, tmpl)
            except ValueError:
                continue
        if dt is None:
            tmpl = "could not parse W3CDTF datetime string '%s'"
            raise ValueError(tmpl % w3cdtf_str)
        if len(offset_str) == 6:
            return cls._offset_dt(dt, offset_str)
        return dt

    def _set_element_datetime(self, prop_name, value):
        """Set date/time value of child element having `prop_name` to `value`."""
        if not isinstance(value, datetime):
            tmpl = "property requires <type 'datetime.datetime'> object, got %s"
            raise ValueError(tmpl % type(value))
        element = self._get_or_add(prop_name)
        dt_str = value.strftime("%Y-%m-%dT%H:%M:%SZ")
        element.text = dt_str
        if prop_name in ("created", "modified"):
            # These two require an explicit "xsi:type="dcterms:W3CDTF""
            # attribute. The first and last line are a hack required to add
            # the xsi namespace to the root element rather than each child
            # element in which it is referenced
            self.set(qn("xsi:foo"), "bar")
            element.set(qn("xsi:type"), "dcterms:W3CDTF")
            del self.attrib[qn("xsi:foo")]

    def _set_element_text(self, prop_name: str, value: Any) -> None:
        """Set string value of `name` property to `value`."""
        if not isinstance(value, str):
            value = str(value)

        if len(value) > 255:
            tmpl = "exceeded 255 char limit for property, got:\n\n'%s'"
            raise ValueError(tmpl % value)
        element = self._get_or_add(prop_name)
        element.text = value

    def _text_of_element(self, property_name: str) -> str:
        """The text in the element matching `property_name`.

        The empty string if the element is not present or contains no text.
        """
        element = getattr(self, property_name)
        if element is None:
            return ""
        if element.text is None:
            return ""
        return element.text
