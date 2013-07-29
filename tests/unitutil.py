# -*- coding: utf-8 -*-
#
# unitutil.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Utility functions for unit testing"""

import os

from mock import patch


def abspath(relpath):
    thisdir = os.path.split(__file__)[0]
    return os.path.abspath(os.path.join(thisdir, relpath))


def class_mock(q_class_name, request):
    """
    Return a mock patching the class with qualified name *q_class_name*.
    Patch is reversed after calling test returns.
    """
    _patch = patch(q_class_name, autospec=True)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def function_mock(q_function_name, request):
    """
    Return a mock patching the function with qualified name
    *q_function_name*. Patch is reversed after calling test returns.
    """
    _patch = patch(q_function_name)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def initializer_mock(cls, request):
    """
    Return a mock for the __init__ method on *cls* where the patch is
    reversed after pytest uses it.
    """
    _patch = patch.object(cls, '__init__', return_value=None)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def method_mock(cls, method_name, request):
    """
    Return a mock for method *method_name* on *cls* where the patch is
    reversed after pytest uses it.
    """
    _patch = patch.object(cls, method_name)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def var_mock(q_var_name, request):
    """
    Return a mock patching the variable with qualified name *q_var_name*.
    Patch is reversed after calling test returns.
    """
    _patch = patch(q_var_name)
    request.addfinalizer(_patch.stop)
    return _patch.start()
