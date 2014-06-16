# encoding: utf-8

"""
Exceptions used with python-docx.

The base exception class is PythonDocxError.
"""


class PythonDocxError(Exception):
    """Generic error class."""


class InvalidXmlError(PythonDocxError):
    """
    Raised when a value is encountered in the XML that is not valid according
    to the schema.
    """
