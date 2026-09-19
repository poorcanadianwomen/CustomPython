"""abc module for CustomPython OS.

Abstract Base Classes.
"""

from collections.abc import Callable, Hashable, Iterable, Iterator, Reversible
from collections.abc import Container, Collection, Sized, Generator, Coroutine
from collections.abc import AsyncIterable, AsyncIterator, AsyncGenerator, Awaitable
from collections.abc import Buffer, Hashable, ItemsView, KeysView, ValuesView
from collections.abc import Mapping, MutableMapping, MappingView
from collections.abc import MutableSequence, MutableSet, Sequence, Set
from collections.abc import ByteString, Mapping, MutableMapping, Sequence, MutableSequence
from collections.abc import Set, MutableSet, MappingView, ItemsView, KeysView, ValuesView


ABCMeta = type


class ABCMeta(type):
    """Metaclass for abstract base classes."""
    
    _abc_cache = {}
    _abc_negative_cache = {}
    _abc_negative_cache_version = 0
    
    def __new__(mcls, name, bases, namespace, /, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        # Collect abstract methods
        abstracts = {name for name, value in namespace.items()
                     if getattr(value, "__isabstractmethod__", False)}
        for base in bases:
            for name in getattr(base, "__abstractmethods__", set()):
                value = getattr(cls, name, None)
                if getattr(value, "__isabstractmethod__", False):
                    abstracts.add(name)
        cls.__abstractmethods__ = frozenset(abstracts)
        # Set up the class
        cls._abc_cache = {}
        cls._abc_negative_cache = {}
        cls._abc_negative_cache_version = 0
        return cls
    
    def register(cls, subclass):
        """Register a virtual subclass."""
        if not isinstance(subclass, type):
            raise TypeError('Expected a type, got', repr(subclass))
        if issubclass(subclass, cls):
            return subclass
        cls._abc_registry.add(subclass)
        return subclass
    
    def __instancecheck__(cls, instance):
        """Check if instance is an instance of cls."""
        if cls in instance.__class__.__mro__:
            return True
        if cls._abc_negative_cache_version == ABCMeta._abc_invalidation_counter:
            if instance.__class__ in cls._abc_negative_cache:
                return False
        else:
            cls._abc_negative_cache.clear()
            cls._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
        
        for rcls in cls._abc_registry:
            if isinstance(instance, rcls):
                cls._abc_negative_cache.add(instance.__class__)
                return True
        
        for rcls in cls.__subclasses__():
            if isinstance(instance, rcls):
                cls._abc_negative_cache.add(instance.__class__)
                return True
        
        cls._abc_negative_cache.add(instance.__class__)
        return False
    
    def __subclasscheck__(cls, subclass):
        """Check if subclass is a subclass of cls."""
        if subclass in cls.__mro__:
            return True
        if cls._abc_negative_cache_version == ABCMeta._abc_invalidation_counter:
            if subclass in cls._abc_negative_cache:
                return False
        else:
            cls._abc_negative_cache.clear()
            cls._abc_negative_cache_version = ABCMeta._abc_invalidation_counter
        
        for rcls in cls._abc_registry:
            if issubclass(subclass, rcls):
                cls._abc_negative_cache.add(subclass)
                return True
        
        for rcls in cls.__subclasses__():
            if issubclass(subclass, rcls):
                cls._abc_negative_cache.add(subclass)
                return True
        
        cls._abc_negative_cache.add(subclass)
        return False
    
    @classmethod
    def _dump_registry(mcls, filename=None):
        """Debug helper: print registry info."""
        pass


_abc_invalidation_counter = 0


def abstractmethod(funcobj):
    """Decorator to mark a method as abstract."""
    funcobj.__isabstractmethod__ = True
    return funcobj


def abstractclassmethod(funcobj):
    """Decorator to mark a classmethod as abstract."""
    funcobj.__isabstractmethod__ = True
    return classmethod(funcobj)


def abstractstaticmethod(funcobj):
    """Decorator to mark a staticmethod as abstract."""
    funcobj.__isabstractmethod__ = True
    return staticmethod(funcobj)


def abstractproperty(funcobj):
    """Decorator to mark a property as abstract."""
    funcobj.__isabstractmethod__ = True
    return property(funcobj)


def get_cache_token():
    """Return the current ABC cache token."""
    return ABCMeta._abc_invalidation_counter


def update_abstractmethods(cls):
    """Force the set of abstract methods to be updated."""
    pass


class ABC(metaclass=ABCMeta):
    """Helper class for abstract base classes."""
    __slots__ = ()


class ABCMeta(type):
    """Metaclass for ABCs."""
    
    _abc_registry = set()
    _abc_cache = {}
    _abc_negative_cache = {}
    _abc_negative_cache_version = 0


# Register some ABCs
for cls in [Hashable, Iterable, Iterator, Reversible, Generator, Coroutine,
            AsyncIterable, AsyncIterator, AsyncGenerator, Awaitable, Container,
            Collection, Sized, Set, MutableSet, Mapping, MutableMapping,
            MappingView, ItemsView, KeysView, ValuesView, Sequence,
            MutableSequence, ByteString, Buffer, Callable]:
    try:
        ABCMeta.register(ABC, cls)
    except TypeError:
        pass
