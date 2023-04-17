from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from datetime import datetime, timedelta
import re

from docx.compat import is_string
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.oxml.xmlchemy import BaseOxmlElement, ZeroOrOne


class CT_ExtendedProperties(BaseOxmlElement):
    """
    ``<Properties>`` element, the root element of the Extended Properties
    part stored as ``/docProps/app.xml``. Implements the Extended document metadata
    elements. String elements resolve to an empty string ('') if the element is
    not present in the XML.
    """
    total_time = ZeroOrOne('Properties', successors=())

    _extendedProperties_tmpl = (
        '<Properties %s/>\n' % nsdecls('xmlns', 'vt')
    )

    @classmethod
    def new(cls):
        """
        Return a new ``<Properties>`` element
        """
        xml = cls._extendedProperties_tmpl
        extended_properties = parse_xml(xml)
        return extended_properties

    @property
    def properties(self):
        """
        The text in the `Template` child element.
        """
        return self._text_of_element('Pro[erties')

    # @total_time.setter
    # def total_time(self, value):
    #     """
    #     Set revision property to string value of integer *value*.
    #     """
    #     if not isinstance(value, str) or value < 1:
    #         tmpl = "str req, got '%s'"
    #         raise ValueError(tmpl % value)
    #     total_time = self.get_or_add_total_time()
    #     total_time.text = str(value)
    @properties.setter
    def properties(self, value):
        self._set_element_text('subject', value)

    # @property
    # def appVersion_text(self):
    #     """
    #     The text in the `AppVersion` child element.
    #     """
    #     return self._text_of_element('appVersion')

    # @appVersion_text.setter
    # def appVersion_text(self, value):
    #     self._set_element_text('appVersion', value)

    # @property
    # def company_text(self):
    #     """
    #     The text in the `Company` child element.
    #     """
    #     return self._text_of_element('company')

    # @company_text.setter
    # def company_text(self, value):
    #     self._set_element_text('company', value)

    # @property
    # def contentStatus_text(self):
    #     """
    #     The text in the `ContentStatus` child element.
    #     """
    #     return self._text_of_element('contentStatus')

    # @contentStatus_text.setter
    # def contentStatus_text(self, value):
    #     self._set_element_text('contentStatus', value)
        
    # @property
    # def totalTime_text(self):
    #     """
    #     The text in the `TotalTime` child element.
    #     """
    #     return self._text_of_element('totalTime')

    # @totalTime_text.setter
    # def totalTime_text(self, value):
    #     self._set_element_text('totalTime', value)

    # @property
    # def created_datetime(self):
    #     """
    #     The datetime value of the `dcterms:created` child element.
    #     """
    #     return self._datetime_of_element('created')

    # @created_datetime.setter
    # def created_datetime(self, value):
    #     self._set_element_datetime('created', value)

    # @property
    # def lastModifiedBy_text(self):
    #     """
    #     The last_modified_by value of the child element.
    #     """
    #     return self._text_of_element('lastModifiedBy')
    
    # @lastModifiedBy_text.setter
    # def lastModifiedBy_text(self, value):
    #     self._set_element_text('lastModifiedBy', value)

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
        """
        Return element returned by 'get_or_add_' method for *prop_name*.
        """
        get_or_add_method_name = 'get_or_add_%s' % prop_name
        get_or_add_method = getattr(self, get_or_add_method_name)
        element = get_or_add_method()
        return element

    @classmethod
    def _offset_dt(cls, dt, offset_str):
        """
        Return a |datetime| instance that is offset from datetime *dt* by
        the timezone offset specified in *offset_str*, a string like
        ``'-07:00'``.
        """
        match = cls._offset_pattern.match(offset_str)
        if match is None:
            raise ValueError(
                "'%s' is not a valid offset string" % offset_str
            )
        sign, hours_str, minutes_str = match.groups()
        sign_factor = -1 if sign == '+' else 1
        hours = int(hours_str) * sign_factor
        minutes = int(minutes_str) * sign_factor
        td = timedelta(hours=hours, minutes=minutes)
        return dt + td

    _offset_pattern = re.compile(r'([+-])(\d\d):(\d\d)')

    @classmethod
    def _parse_W3CDTF_to_datetime(cls, w3cdtf_str):
        # valid W3CDTF date cases:
        # yyyy e.g. '2003'
        # yyyy-mm e.g. '2003-12'
        # yyyy-mm-dd e.g. '2003-12-31'
        # UTC timezone e.g. '2003-12-31T10:14:55Z'
        # numeric timezone e.g. '2003-12-31T10:14:55-08:00'
        templates = (
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d',
            '%Y-%m',
            '%Y',
        )
        # strptime isn't smart enough to parse literal timezone offsets like
        # '-07:30', so we have to do it ourselves
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
        """
        Set date/time value of child element having *prop_name* to *value*.
        """
        if not isinstance(value, datetime):
            tmpl = (
                "property requires <type 'datetime.datetime'> object, got %s"
            )
            raise ValueError(tmpl % type(value))
        element = self._get_or_add(prop_name)
        dt_str = value.strftime('%Y-%m-%dT%H:%M:%SZ')
        element.text = dt_str
        if prop_name in ('created', 'modified'):
            # These two require an explicit 'xsi:type="dcterms:W3CDTF"'
            # attribute. The first and last line are a hack required to add
            # the xsi namespace to the root element rather than each child
            # element in which it is referenced
            self.set(qn('xsi:foo'), 'bar')
            element.set(qn('xsi:type'), 'dcterms:W3CDTF')
            del self.attrib[qn('xsi:foo')]

    def _set_element_text(self, prop_name, value):
        """Set string value of *name* property to *value*."""
        if not is_string(value):
            value = str(value)

        if len(value) > 255:
            tmpl = (
                "exceeded 255 char limit for property, got:\n\n'%s'"
            )
            raise ValueError(tmpl % value)
        element = self._get_or_add(prop_name)
        element.text = value

    def _text_of_element(self, property_name):
        """
        Return the text in the element matching *property_name*, or an empty
        string if the element is not present or contains no text.
        """
        element = getattr(self, property_name)
        if element is None:
            return ''
        if element.text is None:
            return ''
        return element.text
