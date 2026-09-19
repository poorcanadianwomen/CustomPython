"""typing module for CustomPython OS.

Provides type hints support.
"""

import sys
import collections.abc


# Type aliases
Any = object()
NoReturn = type(None)
Nothing = type(None)

# Special forms
ClassVar = type(None)
Final = type(None)
Protocol = type(None)
TypeAlias = type(None)

# Built-in types
def NamedTuple(name, fields):
    """Typed version of collections.namedtuple."""
    import collections
    nt = collections.namedtuple(name, [f[0] if isinstance(f, tuple) else f for f in fields])
    return nt


class _SpecialForm:
    """Special form for typing constructs."""
    
    def __init__(self, name):
        self._name = name
    
    def __repr__(self):
        return f'typing.{self._name}'
    
    def __getitem__(self, params):
        return _GenericAlias(self, params)


class _GenericAlias:
    """Generic alias for type hints."""
    
    def __init__(self, origin, params):
        self.__origin__ = origin
        self.__args__ = params if isinstance(params, tuple) else (params,)
    
    def __repr__(self):
        args = ', '.join(repr(a) for a in self.__args__)
        return f'{self.__origin__}[{args}]'
    
    def __getitem__(self, params):
        return _GenericAlias(self, params)


# Special forms
Union = _SpecialForm('Union')
Optional = _SpecialForm('Optional')
Callable = _SpecialForm('Callable')
Type = _SpecialForm('Type')
Tuple = _SpecialForm('Tuple')
List = _SpecialForm('List')
Dict = _SpecialForm('Dict')
Set = _SpecialForm('Set')
FrozenSet = _SpecialForm('FrozenSet')
TypeVar = _SpecialForm('TypeVar')
Generic = _SpecialForm('Generic')
Sequence = _SpecialForm('Sequence')
MutableSequence = _SpecialForm('MutableSequence')
MutableSet = _SpecialForm('MutableSet')
Mapping = _SpecialForm('Mapping')
MutableMapping = _SpecialForm('MutableMapping')
Iterable = _SpecialForm('Iterable')
Iterator = _SpecialForm('Iterator')
Generator = _SpecialForm('Generator')
Coroutine = _SpecialForm('Coroutine')
AsyncIterable = _SpecialForm('AsyncIterable')
AsyncIterator = _SpecialForm('AsyncIterator')
AsyncGenerator = _SpecialForm('AsyncGenerator')
Awaitable = _SpecialForm('Awaitable')
ContextManager = _SpecialForm('ContextManager')
AsyncContextManager = _SpecialForm('AsyncContextManager')
Pattern = _SpecialForm('Pattern')
Match = _SpecialForm('Match')
ByteString = _SpecialForm('ByteString')
Reversible = _SpecialForm('Reversible')
Container = _SpecialForm('Container')
Collection = _SpecialForm('Collection')
Hashable = _SpecialForm('Hashable')
Sized = _SpecialForm('Sized')
Callable = _SpecialForm('Callable')
AbstractSet = _SpecialForm('AbstractSet')
MutableSet = _SpecialForm('MutableSet')
MappingView = _SpecialForm('MappingView')
KeysView = _SpecialForm('KeysView')
ItemsView = _SpecialForm('ItemsView')
ValuesView = _SpecialForm('ValuesView')
Deque = _SpecialForm('Deque')
Counter = _SpecialForm('Counter')
ChainMap = _SpecialForm('ChainMap')
Awaitable = _SpecialForm('Awaitable')
Coroutine = _SpecialForm('Coroutine')
AsyncIterable = _SpecialForm('AsyncIterable')
AsyncIterator = _SpecialForm('AsyncIterator')
AsyncGenerator = _SpecialForm('AsyncGenerator')
ContextManager = _SpecialForm('ContextManager')
AsyncContextManager = _SpecialForm('AsyncContextManager')
Pattern = _SpecialForm('Pattern')
Match = _SpecialForm('Match')
ClassVar = _SpecialForm('ClassVar')
Final = _SpecialForm('Final')
Protocol = _SpecialForm('Protocol')
TypeAlias = _SpecialForm('TypeAlias')
ParamSpec = _SpecialForm('ParamSpec')
TypeVarTuple = _SpecialForm('TypeVarTuple')
Unpack = _SpecialForm('Unpack')
Required = _SpecialForm('Required')
NotRequired = _SpecialForm('NotRequired')
TypeGuard = _SpecialForm('TypeGuard')
Never = _SpecialForm('Never')
NoReturn = _SpecialForm('NoReturn')


def NamedTuple(name, fields):
    """Typed version of collections.namedtuple."""
    import collections
    nt = collections.namedtuple(name, [f[0] if isinstance(f, tuple) else f for f in fields])
    return nt


class TypedDict(dict):
    """Typed version of dict."""
    
    def __init_subclass__(cls, **kwargs):
        pass
    
    def __new__(cls, **kwargs):
        return dict.__new__(cls, kwargs)


def get_type_hints(obj, globalns=None, localns=None, include_extras=False):
    """Return type hints for an object."""
    if hasattr(obj, '__annotations__'):
        return obj.__annotations__
    return {}


def cast(typ, val):
    """Cast a value to a type."""
    return val


def assert_type(val, typ):
    """Assert that a value is of a type."""
    if not isinstance(val, typ):
        raise TypeError(f'Expected {typ}, got {type(val)}')
    return val


def reveal_type(typ):
    """Reveal the type of an expression."""
    return typ


def dataclass(cls=None, /, *, init=True, repr=True, eq=True, order=False,
              unsafe_hash=False, frozen=False, match_args=True, kw_only=False,
              slots=False, weakref_slot=False):
    """Typed version of dataclasses.dataclass."""
    import dataclasses
    if cls is None:
        return lambda c: dataclasses.dataclass(
            c, init=init, repr=repr, eq=eq, order=order,
            unsafe_hash=unsafe_hash, frozen=frozen, match_args=match_args,
            kw_only=kw_only, slots=slots, weakref_slot=weakref_slot
        )
    return dataclasses.dataclass(
        cls, init=init, repr=repr, eq=eq, order=order,
        unsafe_hash=unsafe_hash, frozen=frozen, match_args=match_args,
        kw_only=kw_only, slots=slots, weakref_slot=weakref_slot
    )


# Protocol support
class Protocol:
    """Base class for protocol classes."""
    __is_protocol__ = True
    
    def __init_subclass__(cls, **kwargs):
        pass
    
    def __class_getitem__(cls, params):
        return cls


# TypeVar
class TypeVar:
    """A generic type variable."""
    
    def __init__(self, name, *constraints, bound=None, covariant=False,
                 contravariant=False, default=None, has_default=False):
        self.__name__ = name
        self.__constraints__ = constraints
        self.__bound__ = bound
        self.__covariant__ = covariant
        self.__contravariant__ = contravariant
        self.__default__ = default
        self.__has_default__ = has_default
    
    def __repr__(self):
        return self.__name__
    
    def __hash__(self):
        return hash(self.__name__)
    
    def __eq__(self, other):
        if isinstance(other, TypeVar):
            return self.__name__ == other.__name__
        return NotImplemented


# ParamSpec
class ParamSpec:
    """A parameter specification."""
    
    def __init__(self, name, *, default=None, has_default=False):
        self.__name__ = name
        self.__default__ = default
        self.__has_default__ = has_default
    
    def __repr__(self):
        return self.__name__


# TypeVarTuple
class TypeVarTuple:
    """A type variable tuple."""
    
    def __init__(self, name, *, default=None, has_default=False):
        self.__name__ = name
        self.__default__ = default
        self.__has_default__ = has_default
    
    def __repr__(self):
        return self.__name__


# Overload
def overload(func):
    """Decorator for overloaded functions."""
    return func


# NoReturn
class _NoReturn:
    """Indicates that a function never returns."""
    __is_class__ = False


NoReturn = _NoReturn()


# Forward reference
class ForwardRef:
    """Forward reference to a type."""
    
    def __init__(self, arg, is_argument=True):
        self.__arg__ = arg
        self.__forward_evaluated__ = False
    
    def __repr__(self):
        return f'ForwardRef({self.__arg__!r})'
    
    def __hash__(self):
        return hash(self.__arg__)
    
    def __eq__(self, other):
        if isinstance(other, ForwardRef):
            return self.__arg__ == other.__arg__
        return NotImplemented


# Annotated
class Annotated:
    """Annotation with metadata."""
    
    def __class_getitem__(cls, params):
        if not isinstance(params, tuple) or len(params) < 2:
            raise TypeError('Annotated[t, ...] requires at least 2 arguments')
        return cls


# Unpack
class Unpack:
    """Unpack a type."""
    
    def __class_getitem__(cls, params):
        return cls


# Required and NotRequired
class Required:
    """Mark a TypedDict key as required."""
    
    def __class_getitem__(cls, params):
        return cls


class NotRequired:
    """Mark a TypedDict key as not required."""
    
    def __class_getitem__(cls, params):
        return cls


# TypeGuard
class TypeGuard:
    """Type guard for narrowing types."""
    
    def __class_getitem__(cls, params):
        return cls


# Never
class _Never:
    """Type that never matches."""
    __is_class__ = False


Never = _Never()
