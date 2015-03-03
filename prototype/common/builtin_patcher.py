#!/usr/bin/env python
# -*- coding: utf-8 -*

#  This code is originally https://gist.github.com/mahmoudimus/295200
# The implementation of StringFormat(https://github.com/florentx/stringformat) is also helpful.

# found this from Armin R. on Twitter, what a beautiful gem ;)
import ctypes
from types import DictProxyType


# figure out size of _Py_ssize_t
if hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
    _Py_ssize_t = ctypes.c_int64
else:
    _Py_ssize_t = ctypes.c_int


# regular python
class _PyObject(ctypes.Structure):
    pass


_PyObject._fields_ = [
    ('ob_refcnt', _Py_ssize_t),
    ('ob_type', ctypes.POINTER(_PyObject))
]


class _DictProxy(_PyObject):
    _fields_ = [('dict', ctypes.POINTER(_PyObject))]


def _reveal_dict(proxy):
    if not isinstance(proxy, DictProxyType):
        raise TypeError('dictproxy expected')
    dp = _DictProxy.from_address(id(proxy))
    ns = {}
    ctypes.pythonapi.PyDict_SetItem(ctypes.py_object(ns),
                                    ctypes.py_object(None),
                                    dp.dict)
    return ns[None]


def _get_class_dict(cls):
    d = getattr(cls, '__dict__', None)
    if d is None:
        raise TypeError('given class does not have a dictionary')
    if isinstance(d, DictProxyType):
        return _reveal_dict(d)
    return d


def attach(typ, name, value):
    _get_class_dict(typ)[name] = value


def detach(typ, name):
    if name in typ.__dict__:
        del _get_class_dict(typ)[name]
