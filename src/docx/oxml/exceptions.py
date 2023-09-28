"""Exceptions for oxml sub-package."""


class XmlchemyError(Exception):
    """Generic error class."""


class InvalidXmlError(XmlchemyError):
    """Raised when invalid XML is encountered, such as on attempt to access a missing
    required child element."""
