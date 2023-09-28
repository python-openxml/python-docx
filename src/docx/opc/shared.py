"""Objects shared by opc modules."""


class CaseInsensitiveDict(dict):
    """Mapping type that behaves like dict except that it matches without respect to the
    case of the key.

    E.g. cid['A'] == cid['a']. Note this is not general-purpose, just complete enough to
    satisfy opc package needs. It assumes str keys, and that it is created empty; keys
    passed in constructor are not accounted for
    """

    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(key.lower())

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(key.lower())

    def __setitem__(self, key, value):
        return super(CaseInsensitiveDict, self).__setitem__(key.lower(), value)


def cls_method_fn(cls: type, method_name: str):
    """Return method of `cls` having `method_name`."""
    return getattr(cls, method_name)


def lazyproperty(f):
    """@lazyprop decorator.

    Decorated method will be called only on first access to calculate a cached property
    value. After that, the cached value is returned.
    """
    cache_attr_name = "_%s" % f.__name__  # like '_foobar' for prop 'foobar'
    docstring = f.__doc__

    def get_prop_value(obj):
        try:
            return getattr(obj, cache_attr_name)
        except AttributeError:
            value = f(obj)
            setattr(obj, cache_attr_name, value)
            return value

    return property(get_prop_value, doc=docstring)
