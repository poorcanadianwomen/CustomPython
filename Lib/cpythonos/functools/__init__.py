"""functools module for CustomPython OS.

Higher-order functions and operations on callable objects.
"""

import sys
import types
from reprlib import recursive_repr


WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__annotations__',
                       '__doc__')
WRAPPER_UPDATES = ('__dict__',)
_update_wrapper = None


def update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function."""
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    wrapper.__wrapped__ = wrapped
    return wrapper


WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__annotations__',
                       '__doc__')
WRAPPER_UPDATES = ('__dict__',)


def wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    """Decorator to update wrapper function to look like wrapped function."""
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)


def partial(func, *args, **keywords):
    """Partial function application."""
    if not callable(func):
        raise TypeError("the first argument must be callable")

    class partial(func.__class__):
        """Partial function application."""
        
        __slots__ = ('func', 'args', 'keywords', '__dict__', '__wrapped__')
        
        def __new__(cls, func, *args, **keywords):
            if not callable(func):
                raise TypeError("the first argument must be callable")
            
            p = object.__new__(cls)
            p.func = func
            p.args = args
            p.keywords = keywords
            return p
        
        def __call__(self, *args, **keywords):
            newkeywords = self.keywords.copy()
            newkeywords.update(keywords)
            return self.func(*self.args, *args, **newkeywords)
        
        def __repr__(self):
            return f"functools.partial({self.func.__name__}, {', '.join(map(repr, self.args))})"
        
        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            return types.MethodType(self, obj)
    
    return partial(func, *args, **keywords)


class cached_property:
    """A property that is only computed once per instance."""
    
    def __init__(self, func):
        self.func = func
        self.attrname = func.__name__
        self.__doc__ = func.__doc__
    
    def __set_name__(self, owner, name):
        self.attrname = name
    
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        try:
            cache = instance.__dict__
        except AttributeError:
            cache = {}
            instance.__dict__ = cache
        val = cache.get(self.attrname, _NOT_FOUND)
        if val is _NOT_FOUND:
            val = self.func(instance)
            cache[self.attrname] = val
        return val


_NOT_FOUND = object()


class lru_cache:
    """Least-recently-used cache decorator."""
    
    def __init__(self, maxsize=128, typed=False):
        if maxsize is None or callable(maxsize):
            wrapper = partial(self.__init__, maxsize=128, typed=False)
            wrapper.__wrapped__ = self
            self = wrapper
            self.maxsize = 128
            self.typed = False
            return
        self.maxsize = maxsize
        self.typed = typed
        self.cache = {}
        self.hits = 0
        self.misses = 0
        self.order = []
    
    def __call__(self, func):
        self.func = func
        self.__wrapped__ = func
        self.__doc__ = func.__doc__
        self.__name__ = func.__name__
        self.__qualname__ = func.__qualname__
        self.cache = {}
        self.hits = 0
        self.misses = 0
        self.order = []
        return self
    
    def __call__(self, *args, **kwargs):
        key = args + tuple(sorted(kwargs.items()))
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        
        result = self.func(*args, **kwargs)
        
        if len(self.cache) >= self.maxsize:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = result
        self.order.append(key)
        self.misses += 1
        return result
    
    def cache_info(self):
        """Return cache statistics."""
        return {
            'hits': self.hits,
            'misses': self.misses,
            'maxsize': self.maxsize,
            'currsize': len(self.cache)
        }
    
    def cache_clear(self):
        """Clear the cache."""
        self.cache.clear()
        self.order.clear()
        self.hits = 0
        self.misses = 0


def lru_cache(maxsize=128, typed=False):
    """Least-recently-used cache decorator."""
    def decorator(func):
        return _lru_cache_wrapper(func, maxsize, typed)
    return decorator


def _lru_cache_wrapper(func, maxsize, typed):
    """Internal LRU cache wrapper."""
    cache = {}
    order = []
    hits = 0
    misses = 0
    
    def wrapper(*args, **kwargs):
        nonlocal hits, misses
        key = args + tuple(sorted(kwargs.items()))
        if key in cache:
            hits += 1
            return cache[key]
        
        result = func(*args, **kwargs)
        
        if maxsize and len(cache) >= maxsize:
            oldest = order.pop(0)
            del cache[oldest]
        
        cache[key] = result
        order.append(key)
        misses += 1
        return result
    
    def cache_info():
        return {
            'hits': hits,
            'misses': misses,
            'maxsize': maxsize,
            'currsize': len(cache)
        }
    
    def cache_clear():
        nonlocal hits, misses
        cache.clear()
        order.clear()
        hits = 0
        misses = 0
    
    wrapper.cache_info = cache_info
    wrapper.cache_clear = cache_clear
    wrapper.__wrapped__ = func
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__qualname__ = func.__qualname__
    return wrapper


def reduce(function, iterable, initializer=None):
    """Apply a function of two arguments cumulatively to the items."""
    it = iter(iterable)
    if initializer is None:
        try:
            value = next(it)
        except StopIteration:
            raise TypeError("reduce() of empty iterable with no initial value")
    else:
        value = initializer
    for element in it:
        value = function(value, element)
    return value


def cmp_to_key(mycmp):
    """Convert a comparison function to a key function."""
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
            self.args = args
        
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def total_ordering(cls):
    """Class decorator that fills in missing ordering methods."""
    convert = {
        '__lt__': [('__gt__', lambda self, other: not (self < other or self == other)),
                   ('__le__', lambda self, other: self < other or self == other),
                   ('__ge__', lambda self, other: not self < other)],
        '__gt__': [('__lt__', lambda self, other: not (self > other or self == other)),
                   ('__ge__', lambda self, other: self > other or self == other),
                   ('__le__', lambda self, other: not self > other)],
        '__le__': [('__ge__', lambda self, other: not (self <= other or self == other)),
                   ('__lt__', lambda self, other: self <= other and self != other),
                   ('__gt__', lambda self, other: not self <= other)],
        '__ge__': [('__le__', lambda self, other: not (self >= other or self == other)),
                   ('__gt__', lambda self, other: self >= other and self != other),
                   ('__lt__', lambda self, other: not self >= other)],
    }
    
    roots = set(dir(cls)) & set(convert.keys())
    if not roots:
        raise ValueError('must define at least one ordering operation')
    
    root = min(roots)
    for opname, conversion in convert[root].items():
        if opname not in roots:
            setattr(cls, opname, conversion)
    
    return cls


def singledispatch(func):
    """Single-dispatch generic function decorator."""
    registry = {}
    registry[object] = func
    
    def wrapper(*args, **kwargs):
        if not args:
            raise TypeError(f'{func.__name__} requires at least 1 argument')
        arg = args[0]
        f = registry.get(type(arg), registry[object])
        return f(*args, **kwargs)
    
    def register(type_, func=None):
        if func is None:
            def decorator(f):
                registry[type_] = f
                return f
            return decorator
        registry[type_] = func
        return func
    
    wrapper.register = register
    wrapper.__wrapped__ = func
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__qualname__ = func.__qualname__
    wrapper.registry = registry
    return wrapper


def partialmethod(func, *args, **keywords):
    """Return a new partialmethod descriptor for func."""
    def _func(self, *method_args, **method_keywords):
        new_keywords = keywords.copy()
        new_keywords.update(method_keywords)
        return func(self, *args, *method_args, **new_keywords)
    
    _func.func = func
    _func.args = args
    _func.keywords = keywords
    return _func


class reduce:
    """Reduce a function over an iterable."""
    
    def __init__(self, function, iterable, initializer=None):
        self.function = function
        self.iterable = iterable
        self.initializer = initializer
    
    def __call__(self):
        return reduce(self.function, self.iterable, self.initializer)
