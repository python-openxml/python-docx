# encoding: utf-8

"""
Provides objects that can characterize image streams as to content type and
size, as a required step in including them in a document.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.image.bmp import Bmp
from docx.image.gif import Gif
from docx.image.jpeg import Exif, Jfif
from docx.image.png import Png
from docx.image.tiff import Tiff


SIGNATURES = (
    # class, offset, signature_bytes
    (Png, 0, b"\x89PNG\x0D\x0A\x1A\x0A"),
    (Jfif, 6, b"JFIF"),
    (Exif, 6, b"Exif"),
    (Gif, 0, b"GIF87a"),
    (Gif, 0, b"GIF89a"),
    (Tiff, 0, b"MM\x00*"),  # big-endian (Motorola) TIFF
    (Tiff, 0, b"II*\x00"),  # little-endian (Intel) TIFF
    (Bmp, 0, b"BM"),
)
