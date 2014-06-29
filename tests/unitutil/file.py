# encoding: utf-8

"""
Utility functions for loading files for unit testing
"""

import os


_thisdir = os.path.split(__file__)[0]
test_file_dir = os.path.abspath(os.path.join(_thisdir, '..', 'test_files'))


def abspath(relpath):
    thisdir = os.path.split(__file__)[0]
    return os.path.abspath(os.path.join(thisdir, relpath))


def absjoin(*paths):
    return os.path.abspath(os.path.join(*paths))


def docx_path(name):
    """
    Return the absolute path to test .docx file with root name *name*.
    """
    return absjoin(test_file_dir, '%s.docx' % name)


def test_file(name):
    """
    Return the absolute path to test file having *name*.
    """
    return absjoin(test_file_dir, name)
