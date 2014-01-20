# encoding: utf-8


class InvalidImageStreamError(Exception):
    """
    The recognized image stream appears to be corrupted
    """


class UnexpectedEndOfFileError(Exception):
    """
    EOF was unexpectedly encountered while reading an image stream.
    """


class UnrecognizedImageError(Exception):
    """
    The provided image stream could not be recognized.
    """
