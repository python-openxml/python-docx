# encoding: utf-8

"""
Relationship-related objects.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .oxml import CT_Relationships


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
        for rel in sorted(self.values(), key=lambda r: r._rId):
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
