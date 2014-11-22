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


def snippet_seq(name, offset=0, count=1024):
    """
    Return a tuple containing the unicode text snippets read from the snippet
    file having *name*. Snippets are delimited by a blank line. If specified,
    *count* snippets starting at *offset* are returned.
    """
    path = os.path.join(test_file_dir, 'snippets', '%s.txt' % name)
    with open(path, 'rb') as f:
        text = f.read().decode('utf-8')
    snippets = text.split('\n\n')
    start, end = offset, offset+count
    return tuple(snippets[start:end])


def snippet_text(snippet_file_name):
    """
    Return the unicode text read from the test snippet file having
    *snippet_file_name*.
    """
    snippet_file_path = os.path.join(
        test_file_dir, 'snippets', '%s.txt' % snippet_file_name
    )
    with open(snippet_file_path, 'rb') as f:
        snippet_bytes = f.read()
    return snippet_bytes.decode('utf-8')


def test_file(name):
    """
    Return the absolute path to test file having *name*.
    """
    return absjoin(test_file_dir, name)
