# encoding: utf-8

"""
Utility functions for unit testing
"""

import os

from mock import create_autospec, Mock, patch, PropertyMock

from docx.oxml.xmlchemy import serialize_for_reading


_thisdir = os.path.split(__file__)[0]
test_file_dir = os.path.abspath(os.path.join(_thisdir, 'test_files'))


def abspath(relpath):
    thisdir = os.path.split(__file__)[0]
    return os.path.abspath(os.path.join(thisdir, relpath))


def actual_xml(elm):
    return serialize_for_reading(elm)


def absjoin(*paths):
    return os.path.abspath(os.path.join(*paths))


def docx_path(name):
    """
    Return the absolute path to test .docx file with root name *name*.
    """
    return absjoin(_thisdir, 'test_files', '%s.docx' % name)


def test_file(name):
    """
    Return the absolute path to test file having *name*.
    """
    return absjoin(_thisdir, 'test_files', name)


# ===========================================================================
# pytest mocking helpers
# ===========================================================================


def class_mock(request, q_class_name, autospec=True, **kwargs):
    """
    Return a mock patching the class with qualified name *q_class_name*.
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


def function_mock(request, q_function_name, **kwargs):
    """
    Return a mock patching the function with qualified name
    *q_function_name*. Patch is reversed after calling test returns.
    """
    _patch = patch(q_function_name, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def initializer_mock(request, cls):
    """
    Return a mock for the __init__ method on *cls* where the patch is
    reversed after pytest uses it.
    """
    _patch = patch.object(cls, '__init__', return_value=None)
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
    return create_autospec(
        cls, _name=name, spec_set=spec_set, instance=True, **kwargs
    )


def loose_mock(request, name=None, **kwargs):
    """
    Return a "loose" mock, meaning it has no spec to constrain calls on it.
    Additional keyword arguments are passed through to Mock(). If called
    without a name, it is assigned the name of the fixture.
    """
    if name is None:
        name = request.fixturename
    return Mock(name=name, **kwargs)


def method_mock(request, cls, method_name, **kwargs):
    """
    Return a mock for method *method_name* on *cls* where the patch is
    reversed after pytest uses it.
    """
    _patch = patch.object(cls, method_name, **kwargs)
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
