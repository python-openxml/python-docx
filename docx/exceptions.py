# encoding: utf-8

"""
Exceptions used with python-docx.

The base exception class is PythonDocxError.
"""


class PythonDocxError(Exception):
    """
    Generic error class.
    """


class InvalidXmlError(PythonDocxError):
    """
    Raised when invalid XML is encountered, such as on attempt to access a
    missing required child element
    """
