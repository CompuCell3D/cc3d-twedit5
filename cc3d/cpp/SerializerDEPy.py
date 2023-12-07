# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.1.1
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _SerializerDEPy
else:
    import _SerializerDEPy

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "this":
            set(self, name, value)
        elif name == "thisown":
            self.this.own(value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _SerializerDEPy.delete_SwigPyIterator

    def value(self):
        return _SerializerDEPy.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _SerializerDEPy.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _SerializerDEPy.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _SerializerDEPy.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _SerializerDEPy.SwigPyIterator_equal(self, x)

    def copy(self):
        return _SerializerDEPy.SwigPyIterator_copy(self)

    def next(self):
        return _SerializerDEPy.SwigPyIterator_next(self)

    def __next__(self):
        return _SerializerDEPy.SwigPyIterator___next__(self)

    def previous(self):
        return _SerializerDEPy.SwigPyIterator_previous(self)

    def advance(self, n):
        return _SerializerDEPy.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _SerializerDEPy.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _SerializerDEPy.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _SerializerDEPy.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _SerializerDEPy.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _SerializerDEPy.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _SerializerDEPy.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _SerializerDEPy:
_SerializerDEPy.SwigPyIterator_swigregister(SwigPyIterator)
class vectorint(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _SerializerDEPy.vectorint_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _SerializerDEPy.vectorint___nonzero__(self)

    def __bool__(self):
        return _SerializerDEPy.vectorint___bool__(self)

    def __len__(self):
        return _SerializerDEPy.vectorint___len__(self)

    def __getslice__(self, i, j):
        return _SerializerDEPy.vectorint___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _SerializerDEPy.vectorint___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _SerializerDEPy.vectorint___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _SerializerDEPy.vectorint___delitem__(self, *args)

    def __getitem__(self, *args):
        return _SerializerDEPy.vectorint___getitem__(self, *args)

    def __setitem__(self, *args):
        return _SerializerDEPy.vectorint___setitem__(self, *args)

    def pop(self):
        return _SerializerDEPy.vectorint_pop(self)

    def append(self, x):
        return _SerializerDEPy.vectorint_append(self, x)

    def empty(self):
        return _SerializerDEPy.vectorint_empty(self)

    def size(self):
        return _SerializerDEPy.vectorint_size(self)

    def swap(self, v):
        return _SerializerDEPy.vectorint_swap(self, v)

    def begin(self):
        return _SerializerDEPy.vectorint_begin(self)

    def end(self):
        return _SerializerDEPy.vectorint_end(self)

    def rbegin(self):
        return _SerializerDEPy.vectorint_rbegin(self)

    def rend(self):
        return _SerializerDEPy.vectorint_rend(self)

    def clear(self):
        return _SerializerDEPy.vectorint_clear(self)

    def get_allocator(self):
        return _SerializerDEPy.vectorint_get_allocator(self)

    def pop_back(self):
        return _SerializerDEPy.vectorint_pop_back(self)

    def erase(self, *args):
        return _SerializerDEPy.vectorint_erase(self, *args)

    def __init__(self, *args):
        _SerializerDEPy.vectorint_swiginit(self, _SerializerDEPy.new_vectorint(*args))

    def push_back(self, x):
        return _SerializerDEPy.vectorint_push_back(self, x)

    def front(self):
        return _SerializerDEPy.vectorint_front(self)

    def back(self):
        return _SerializerDEPy.vectorint_back(self)

    def assign(self, n, x):
        return _SerializerDEPy.vectorint_assign(self, n, x)

    def resize(self, *args):
        return _SerializerDEPy.vectorint_resize(self, *args)

    def insert(self, *args):
        return _SerializerDEPy.vectorint_insert(self, *args)

    def reserve(self, n):
        return _SerializerDEPy.vectorint_reserve(self, n)

    def capacity(self):
        return _SerializerDEPy.vectorint_capacity(self)
    __swig_destroy__ = _SerializerDEPy.delete_vectorint

# Register vectorint in _SerializerDEPy:
_SerializerDEPy.vectorint_swigregister(vectorint)
class vectorstring(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _SerializerDEPy.vectorstring_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _SerializerDEPy.vectorstring___nonzero__(self)

    def __bool__(self):
        return _SerializerDEPy.vectorstring___bool__(self)

    def __len__(self):
        return _SerializerDEPy.vectorstring___len__(self)

    def __getslice__(self, i, j):
        return _SerializerDEPy.vectorstring___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _SerializerDEPy.vectorstring___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _SerializerDEPy.vectorstring___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _SerializerDEPy.vectorstring___delitem__(self, *args)

    def __getitem__(self, *args):
        return _SerializerDEPy.vectorstring___getitem__(self, *args)

    def __setitem__(self, *args):
        return _SerializerDEPy.vectorstring___setitem__(self, *args)

    def pop(self):
        return _SerializerDEPy.vectorstring_pop(self)

    def append(self, x):
        return _SerializerDEPy.vectorstring_append(self, x)

    def empty(self):
        return _SerializerDEPy.vectorstring_empty(self)

    def size(self):
        return _SerializerDEPy.vectorstring_size(self)

    def swap(self, v):
        return _SerializerDEPy.vectorstring_swap(self, v)

    def begin(self):
        return _SerializerDEPy.vectorstring_begin(self)

    def end(self):
        return _SerializerDEPy.vectorstring_end(self)

    def rbegin(self):
        return _SerializerDEPy.vectorstring_rbegin(self)

    def rend(self):
        return _SerializerDEPy.vectorstring_rend(self)

    def clear(self):
        return _SerializerDEPy.vectorstring_clear(self)

    def get_allocator(self):
        return _SerializerDEPy.vectorstring_get_allocator(self)

    def pop_back(self):
        return _SerializerDEPy.vectorstring_pop_back(self)

    def erase(self, *args):
        return _SerializerDEPy.vectorstring_erase(self, *args)

    def __init__(self, *args):
        _SerializerDEPy.vectorstring_swiginit(self, _SerializerDEPy.new_vectorstring(*args))

    def push_back(self, x):
        return _SerializerDEPy.vectorstring_push_back(self, x)

    def front(self):
        return _SerializerDEPy.vectorstring_front(self)

    def back(self):
        return _SerializerDEPy.vectorstring_back(self)

    def assign(self, n, x):
        return _SerializerDEPy.vectorstring_assign(self, n, x)

    def resize(self, *args):
        return _SerializerDEPy.vectorstring_resize(self, *args)

    def insert(self, *args):
        return _SerializerDEPy.vectorstring_insert(self, *args)

    def reserve(self, n):
        return _SerializerDEPy.vectorstring_reserve(self, n)

    def capacity(self):
        return _SerializerDEPy.vectorstring_capacity(self)
    __swig_destroy__ = _SerializerDEPy.delete_vectorstring

# Register vectorstring in _SerializerDEPy:
_SerializerDEPy.vectorstring_swigregister(vectorstring)
class SerializeData(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _SerializerDEPy.SerializeData_swiginit(self, _SerializerDEPy.new_SerializeData())
    moduleName = property(_SerializerDEPy.SerializeData_moduleName_get, _SerializerDEPy.SerializeData_moduleName_set)
    moduleType = property(_SerializerDEPy.SerializeData_moduleType_get, _SerializerDEPy.SerializeData_moduleType_set)
    objectName = property(_SerializerDEPy.SerializeData_objectName_get, _SerializerDEPy.SerializeData_objectName_set)
    objectType = property(_SerializerDEPy.SerializeData_objectType_get, _SerializerDEPy.SerializeData_objectType_set)
    fileName = property(_SerializerDEPy.SerializeData_fileName_get, _SerializerDEPy.SerializeData_fileName_set)
    fileFormat = property(_SerializerDEPy.SerializeData_fileFormat_get, _SerializerDEPy.SerializeData_fileFormat_set)
    objectPtr = property(_SerializerDEPy.SerializeData_objectPtr_get, _SerializerDEPy.SerializeData_objectPtr_set)

    def generateXMlStub(self):
        return _SerializerDEPy.SerializeData_generateXMlStub(self)
    __swig_destroy__ = _SerializerDEPy.delete_SerializeData

# Register SerializeData in _SerializerDEPy:
_SerializerDEPy.SerializeData_swigregister(SerializeData)
class SerializerDE(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _SerializerDEPy.SerializerDE_swiginit(self, _SerializerDEPy.new_SerializerDE())

    def init(self, _sim):
        return _SerializerDEPy.SerializerDE_init(self, _sim)
    __swig_destroy__ = _SerializerDEPy.delete_SerializerDE

    def serializeConcentrationField(self, _sd):
        return _SerializerDEPy.SerializerDE_serializeConcentrationField(self, _sd)

    def serializeCellField(self, _sd):
        return _SerializerDEPy.SerializerDE_serializeCellField(self, _sd)

    def serializeScalarField(self, _sd):
        return _SerializerDEPy.SerializerDE_serializeScalarField(self, _sd)

    def serializeScalarFieldCellLevel(self, _sd):
        return _SerializerDEPy.SerializerDE_serializeScalarFieldCellLevel(self, _sd)

    def serializeVectorField(self, _sd):
        return _SerializerDEPy.SerializerDE_serializeVectorField(self, _sd)

    def serializeVectorFieldCellLevel(self, _sd):
        return _SerializerDEPy.SerializerDE_serializeVectorFieldCellLevel(self, _sd)

    def loadCellField(self, _sd):
        return _SerializerDEPy.SerializerDE_loadCellField(self, _sd)

    def loadConcentrationField(self, _sd):
        return _SerializerDEPy.SerializerDE_loadConcentrationField(self, _sd)

    def loadScalarField(self, _sd):
        return _SerializerDEPy.SerializerDE_loadScalarField(self, _sd)

    def loadScalarFieldCellLevel(self, _sd):
        return _SerializerDEPy.SerializerDE_loadScalarFieldCellLevel(self, _sd)

    def loadVectorField(self, _sd):
        return _SerializerDEPy.SerializerDE_loadVectorField(self, _sd)

    def loadVectorFieldCellLevel(self, _sd):
        return _SerializerDEPy.SerializerDE_loadVectorFieldCellLevel(self, _sd)
    serializedDataVec = property(_SerializerDEPy.SerializerDE_serializedDataVec_get, _SerializerDEPy.SerializerDE_serializedDataVec_set)

# Register SerializerDE in _SerializerDEPy:
_SerializerDEPy.SerializerDE_swigregister(SerializerDE)
