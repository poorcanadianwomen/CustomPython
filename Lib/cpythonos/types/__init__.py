"""types module for CustomPython OS.

Dynamic type creation and names for built-in types.
"""


# Type names
FunctionType = type(lambda: None)
LambdaType = type(lambda: None)
CodeType = type((lambda: None).__code__)
CellType = type((lambda: None.__closure__ or (None,))[0] if (lambda: None).__closure__ else None)
MethodType = type((lambda: None).__self__)
BuiltinFunctionType = type(len)
BuiltinMethodType = type([].append)
WrapperDescriptorType = type(object.__init__)
MethodWrapperType = type(object().__init__)
MethodDescriptorType = type(dict.items)
ClassMethodDescriptorType = type(dict.fromkeys)
ModuleType = type(sys)
GetSetDescriptorType = type(type.__dict__['__dict__'])
MemberDescriptorType = type(type.__dict__['__bases__'])
TracebackType = type(None.__traceback__)
FrameType = type(None.__frame__)
GeneratorType = type((yield))
CoroutineType = type((yield).__await__())
AsyncGeneratorType = type((yield).__aiter__())
MappingProxyType = type(type.__dict__)
SimpleNamespace = type(sys.modules[__name__])

# Dynamic type creation
def new_class(name, bases=(), kwds=None, exec_body=None):
    """Create a new class dynamically."""
    if kwds is None:
        kwds = {}
    
    if exec_body is None:
        exec_body = lambda ns: None
    
    metaclass = kwds.pop('metaclass', type)
    
    if bases:
        base = bases[0]
        if isinstance(base, type):
            metaclass = type(base)
    
    namespace = metaclass.__prepare__(name, bases)
    exec_body(namespace)
    return metaclass(name, bases, namespace)


def prepare_class(name, bases=(), kwds=None):
    """Prepare a class namespace."""
    if kwds is None:
        kwds = {}
    
    metaclass = kwds.pop('metaclass', type)
    
    if bases:
        base = bases[0]
        if isinstance(base, type):
            metaclass = type(base)
    
    return metaclass.__prepare__(name, bases), metaclass


def resolve_bases(bases):
    """Resolve MRO bases dynamically."""
    return bases


def get_original_bases(cls):
    """Return the bases of a class."""
    return cls.__bases__


def resolve_mro_entry(resolved_bases, base):
    """Resolve a single MRO entry."""
    return base


# Utility functions
def isclass(object):
    """Return True if the object is a class."""
    return isinstance(object, type)


def issubclass(classinfo, classinfo2):
    """Return True if classinfo is a subclass of classinfo2."""
    return isinstance(classinfo, type) and issubclass(classinfo, classinfo2)


def getattr_static(obj, attr, default=<object object at 0x7f...>):
    """Retrieve attributes without triggering descriptors."""
    try:
        return getattr(obj, attr)
    except AttributeError:
        if default is <object object at 0x7f...>:
            raise
        return default


def issubclass(classinfo, classinfo2):
    """Return True if classinfo is a subclass of classinfo2."""
    if isinstance(classinfo, type):
        return classinfo2 in classinfo.__mro__
    return False


class DynamicClassAttribute:
    """Descriptor to define attributes that behave differently in class and instance contexts."""
    
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or (fget.__doc__ if fget else None)
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.fget(obj)
    
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)
    
    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)
    
    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)
    
    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)
    
    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


class WrapperDescriptor:
    """Descriptor for wrapper types."""
    
    def __init__(self, name, doc):
        self.__name__ = name
        self.__doc__ = doc
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return MethodType(self, obj)


class MethodWrapper:
    """Descriptor for bound methods."""
    
    def __init__(self, name, doc):
        self.__name__ = name
        self.__doc__ = doc
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self


class MethodDescriptor:
    """Descriptor for methods defined in C."""
    
    def __init__(self, name, doc):
        self.__name__ = name
        self.__doc__ = doc
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self


class ClassMethodDescriptor:
    """Descriptor for class methods defined in C."""
    
    def __init__(self, name, doc):
        self.__name__ = name
        self.__doc__ = doc
    
    def __get__(self, obj, objtype=None):
        if objtype is None:
            objtype = type(obj)
        return self


class GetSetDescriptor:
    """Descriptor for getset attributes."""
    
    def __init__(self, name, doc):
        self.__name__ = name
        self.__doc__ = doc
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self


class MemberDescriptor:
    """Descriptor for member attributes."""
    
    def __init__(self, name, doc):
        self.__name__ = name
        self.__doc__ = doc
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self
