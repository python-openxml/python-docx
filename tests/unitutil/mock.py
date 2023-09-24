# encoding: utf-8

"""Utility functions wrapping the excellent *mock* library"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

if sys.version_info >= (3, 3):
    from unittest import mock  # noqa
    from unittest.mock import ANY, call, MagicMock  # noqa
    from unittest.mock import create_autospec, Mock, mock_open, patch, PropertyMock
else:
    import mock  # noqa
    from mock import ANY, call, MagicMock  # noqa
    from mock import create_autospec, Mock, patch, PropertyMock


def class_mock(request, q_class_name, autospec=True, **kwargs):
    """Return mock patching class with qualified name *q_class_name*.

    The mock is autospec'ed based on the patched class unless the optional
    argument *autospec* is set to False. Any other keyword arguments are
    passed through to Mock(). Patch is reversed after calling test returns.
    """
    _patch = patch(q_class_name, autospec=autospec, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def cls_attr_mock(request, cls, attr_name, name=None, **kwargs):
    """
    Return a mock for attribute *attr_name* on *cls* where the patch is
    reversed after pytest uses it.
    """
    name = request.fixturename if name is None else name
    _patch = patch.object(cls, attr_name, name=name, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def function_mock(request, q_function_name, autospec=True, **kwargs):
    """Return mock patching function with qualified name *q_function_name*.

    Patch is reversed after calling test returns.
    """
    _patch = patch(q_function_name, autospec=autospec, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def initializer_mock(request, cls, autospec=True, **kwargs):
    """Return mock for __init__() method on *cls*.

    The patch is reversed after pytest uses it.
    """
    _patch = patch.object(
        cls, "__init__", autospec=autospec, return_value=None, **kwargs
    )
    request.addfinalizer(_patch.stop)
    return _patch.start()


def instance_mock(request, cls, name=None, spec_set=True, **kwargs):
    """
    Return a mock for an instance of *cls* that draws its spec from the class
    and does not allow new attributes to be set on the instance. If *name* is
    missing or |None|, the name of the returned |Mock| instance is set to
    *request.fixturename*. Additional keyword arguments are passed through to
    the Mock() call that creates the mock.
    """
    name = name if name is not None else request.fixturename
    return create_autospec(cls, _name=name, spec_set=spec_set, instance=True, **kwargs)


def loose_mock(request, name=None, **kwargs):
    """
    Return a "loose" mock, meaning it has no spec to constrain calls on it.
    Additional keyword arguments are passed through to Mock(). If called
    without a name, it is assigned the name of the fixture.
    """
    if name is None:
        name = request.fixturename
    return Mock(name=name, **kwargs)


def method_mock(request, cls, method_name, autospec=True, **kwargs):
    """Return mock for method *method_name* on *cls*.

    The patch is reversed after pytest uses it.
    """
    _patch = patch.object(cls, method_name, autospec=autospec, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def open_mock(request, module_name, **kwargs):
    """
    Return a mock for the builtin `open()` method in *module_name*.
    """
    target = "%s.open" % module_name
    _patch = patch(target, mock_open(), create=True, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def property_mock(request, cls, prop_name, **kwargs):
    """
    Return a mock for property *prop_name* on class *cls* where the patch is
    reversed after pytest uses it.
    """
    _patch = patch.object(cls, prop_name, new_callable=PropertyMock, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def var_mock(request, q_var_name, **kwargs):
    """
    Return a mock patching the variable with qualified name *q_var_name*.
    Patch is reversed after calling test returns.
    """
    _patch = patch(q_var_name, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()
