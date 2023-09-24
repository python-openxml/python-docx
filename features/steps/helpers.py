# encoding: utf-8

"""
Helper methods and variables for acceptance tests.
"""

import os


def absjoin(*paths):
    return os.path.abspath(os.path.join(*paths))


thisdir = os.path.split(__file__)[0]
scratch_dir = absjoin(thisdir, "../_scratch")

# scratch output docx file -------------
saved_docx_path = absjoin(scratch_dir, "test_out.docx")

bool_vals = {"True": True, "False": False}

test_text = "python-docx was here!"

tri_state_vals = {
    "True": True,
    "False": False,
    "None": None,
}


def test_docx(name):
    """
    Return the absolute path to test .docx file with root name *name*.
    """
    return absjoin(thisdir, "test_files", "%s.docx" % name)


def test_file(name):
    """
    Return the absolute path to file with *name* in test_files directory
    """
    return absjoin(thisdir, "test_files", "%s" % name)
