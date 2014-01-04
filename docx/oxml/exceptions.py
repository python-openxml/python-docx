# encoding: utf-8

"""
Exceptions for oxml sub-package
"""


class ValidationError(Exception):
    """
    Raised when invalid XML is encountered, such as on attempt to access a
    missing required child element
    """
