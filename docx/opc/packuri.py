# encoding: utf-8

"""
Provides the PackURI value type along with some useful known pack URI strings
such as PACKAGE_URI.
"""

import posixpath
import re


class PackURI(str):
    """
    Provides access to pack URI components such as the baseURI and the
    filename slice. Behaves as |str| otherwise.
    """

    _filename_re = re.compile("([a-zA-Z]+)([1-9][0-9]*)?")

    def __new__(cls, pack_uri_str):
        if not pack_uri_str[0] == "/":
            tmpl = "PackURI must begin with slash, got '%s'"
            raise ValueError(tmpl % pack_uri_str)
        return str.__new__(cls, pack_uri_str)

    @staticmethod
    def from_rel_ref(baseURI, relative_ref):
        """
        Return a |PackURI| instance containing the absolute pack URI formed by
        translating *relative_ref* onto *baseURI*.
        """
        joined_uri = posixpath.join(baseURI, relative_ref)
        abs_uri = posixpath.abspath(joined_uri)
        return PackURI(abs_uri)

    @property
    def baseURI(self):
        """
        The base URI of this pack URI, the directory portion, roughly
        speaking. E.g. ``'/ppt/slides'`` for ``'/ppt/slides/slide1.xml'``.
        For the package pseudo-partname '/', baseURI is '/'.
        """
        return posixpath.split(self)[0]

    @property
    def ext(self):
        """
        The extension portion of this pack URI, e.g. ``'xml'`` for
        ``'/word/document.xml'``. Note the period is not included.
        """
        # raw_ext is either empty string or starts with period, e.g. '.xml'
        raw_ext = posixpath.splitext(self)[1]
        return raw_ext[1:] if raw_ext.startswith(".") else raw_ext

    @property
    def filename(self):
        """
        The "filename" portion of this pack URI, e.g. ``'slide1.xml'`` for
        ``'/ppt/slides/slide1.xml'``. For the package pseudo-partname '/',
        filename is ''.
        """
        return posixpath.split(self)[1]

    @property
    def idx(self):
        """
        Return partname index as integer for tuple partname or None for
        singleton partname, e.g. ``21`` for ``'/ppt/slides/slide21.xml'`` and
        |None| for ``'/ppt/presentation.xml'``.
        """
        filename = self.filename
        if not filename:
            return None
        name_part = posixpath.splitext(filename)[0]  # filename w/ext removed
        match = self._filename_re.match(name_part)
        if match is None:
            return None
        if match.group(2):
            return int(match.group(2))
        return None

    @property
    def membername(self):
        """
        The pack URI with the leading slash stripped off, the form used as
        the Zip file membername for the package item. Returns '' for the
        package pseudo-partname '/'.
        """
        return self[1:]

    def relative_ref(self, baseURI):
        """
        Return string containing relative reference to package item from
        *baseURI*. E.g. PackURI('/ppt/slideLayouts/slideLayout1.xml') would
        return '../slideLayouts/slideLayout1.xml' for baseURI '/ppt/slides'.
        """
        # workaround for posixpath bug in 2.6, doesn't generate correct
        # relative path when *start* (second) parameter is root ('/')
        if baseURI == "/":
            relpath = self[1:]
        else:
            relpath = posixpath.relpath(self, baseURI)
        return relpath

    @property
    def rels_uri(self):
        """
        The pack URI of the .rels part corresponding to the current pack URI.
        Only produces sensible output if the pack URI is a partname or the
        package pseudo-partname '/'.
        """
        rels_filename = "%s.rels" % self.filename
        rels_uri_str = posixpath.join(self.baseURI, "_rels", rels_filename)
        return PackURI(rels_uri_str)


PACKAGE_URI = PackURI("/")
CONTENT_TYPES_URI = PackURI("/[Content_Types].xml")
