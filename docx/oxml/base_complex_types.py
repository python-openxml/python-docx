# encoding: utf-8

"""
Simple complex types classes represent base elements
"""

from .xmlchemy import BaseOxmlElement, RequiredAttribute
from .simpletypes import ST_RelationshipId


class CT_Rel(BaseOxmlElement):
    """
    ``<r:id>`` element, defining the rId .
    """
    rId = RequiredAttribute('r:id', ST_RelationshipId)
