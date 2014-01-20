# encoding: utf-8


class InvalidImageStreamError(Exception):
    """
    The recognized image stream appears to be corrupted
    """


class UnrecognizedImageError(Exception):
    """
    The provided image stream could not be recognized.
    """
