"""weakref module for CustomPython OS.

Weak references to objects.
"""

import sys
from _weakref import (
    ref,
    proxy,
    getweakrefcount,
    getweakrefs,
    RefType,
)


class WeakValueDictionary(dict):
    """Dictionary that references values weakly."""
    
    def __init__(self, dict=None, /, **kwargs):
        super().__init__()
        if dict is not None:
            self.update(dict)
        if kwargs:
            self.update(kwargs)
    
    def __setitem__(self, key, value):
        super().__setitem__(key, ref(value, self._remove))
    
    def __getitem__(self, key):
        obj = super().__getitem__(key)()
        if obj is None:
            raise KeyError(key)
        return obj
    
    def __delitem__(self, key):
        super().__delitem__(key)
    
    def _remove(self, ref):
        for key, value in self.items():
            if value is ref:
                super().__delitem__(key)
                break
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
    
    def items(self):
        for key, ref in super().items():
            obj = ref()
            if obj is not None:
                yield key, obj
    
    def values(self):
        for ref in super().values():
            obj = ref()
            if obj is not None:
                yield obj
    
    def keys(self):
        return super().keys()
    
    def __contains__(self, key):
        try:
            ref = super().__getitem__(key)
            return ref() is not None
        except KeyError:
            return False
    
    def pop(self, key, *args):
        try:
            obj = self[key]
            super().__delitem__(key)
            return obj
        except KeyError:
            if args:
                return args[0]
            raise
    
    def popitem(self):
        while True:
            key, ref = super().popitem()
            obj = ref()
            if obj is not None:
                return key, obj
    
    def clear(self):
        super().clear()
    
    def copy(self):
        new = WeakValueDictionary()
        for key, ref in super().items():
            obj = ref()
            if obj is not None:
                new[key] = obj
        return new
    
    def update(self, dict=None, **kwargs):
        if dict is not None:
            for key, value in dict.items():
                self[key] = value
        for key, value in kwargs.items():
            self[key] = value
    
    def setdefault(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default
    
    def __repr__(self):
        items = []
        for key, ref in super().items():
            obj = ref()
            if obj is not None:
                items.append(f'{key!r}: {obj!r}')
        return '{' + ', '.join(items) + '}'


class KeyedRef(ref):
    """Reference with a key for dictionary use."""
    
    def __new__(cls, ob, callback, key):
        self = super().__new__(cls, ob, callback)
        self.__key = key
        return self
    
    @property
    def key(self):
        return self.__key


class WeakKeyDictionary(dict):
    """Dictionary that references keys weakly."""
    
    def __init__(self, dict=None, /, **kwargs):
        super().__init__()
        self.data = {}
        if dict is not None:
            self.update(dict)
        if kwargs:
            self.update(kwargs)
    
    def __setitem__(self, key, value):
        def remove(ref):
            self.data.pop(ref.key, None)
        self.data[id(key)] = KeyedRef(key, remove, id(key))
        super().__setitem__(key, value)
    
    def __getitem__(self, key):
        return super().__getitem__(key)
    
    def __delitem__(self, key):
        super().__delitem__(key)
        self.data.pop(id(key), None)
    
    def __contains__(self, key):
        return super().__contains__(key)
    
    def __iter__(self):
        return super().__iter__()
    
    def __len__(self):
        return super().__len__()
    
    def __repr__(self):
        return f'{type(self).__name__}({dict(self)!r})'
    
    def copy(self):
        return type(self)(self)
    
    def __ior__(self, other):
        for key, value in other.items():
            self[key] = value
        return self


class WeakSet:
    """Set that references elements weakly."""
    
    def __init__(self, data=None):
        self.data = set()
        if data is not None:
            for item in data:
                self.add(item)
    
    def add(self, item):
        def remove(ref):
            self.data.discard(ref)
        self.data.add(ref(item, remove))
    
    def discard(self, item):
        for ref in self.data:
            if ref() is item:
                self.data.discard(ref)
                return
    
    def remove(self, item):
        for ref in self.data:
            if ref() is item:
                self.data.discard(ref)
                return
        raise KeyError(item)
    
    def pop(self):
        for ref in self.data:
            obj = ref()
            if obj is not None:
                self.data.discard(ref)
                return obj
        raise KeyError('pop from an empty WeakSet')
    
    def clear(self):
        self.data.clear()
    
    def copy(self):
        new = WeakSet()
        for ref in self.data:
            obj = ref()
            if obj is not None:
                new.add(obj)
        return new
    
    def __contains__(self, item):
        for ref in self.data:
            if ref() is item:
                return True
        return False
    
    def __iter__(self):
        for ref in self.data:
            obj = ref()
            if obj is not None:
                yield obj
    
    def __len__(self):
        return len([ref for ref in self.data if ref() is not None])
    
    def __repr__(self):
        return f'WeakSet({list(self)!r})'
    
    def __or__(self, other):
        result = WeakSet(self)
        for item in other:
            result.add(item)
        return result
    
    def __and__(self, other):
        result = WeakSet()
        for item in self:
            if item in other:
                result.add(item)
        return result
    
    def __sub__(self, other):
        result = WeakSet(self)
        for item in other:
            result.discard(item)
        return result
    
    def __xor__(self, other):
        result = WeakSet()
        for item in self:
            if item not in other:
                result.add(item)
        for item in other:
            if item not in self:
                result.add(item)
        return result
    
    def __ior__(self, other):
        for item in other:
            self.add(item)
        return self
    
    def __iand__(self, other):
        for item in list(self):
            if item not in other:
                self.discard(item)
        return self
    
    def __isub__(self, other):
        for item in other:
            self.discard(item)
        return self
    
    def __ixor__(self, other):
        to_remove = set()
        to_add = set()
        for item in other:
            if item in self:
                to_remove.add(item)
            else:
                to_add.add(item)
        for item in to_remove:
            self.discard(item)
        for item in to_add:
            self.add(item)
        return self


def finalize(obj, func, *args, **kwargs):
    """Return a callable to destroy obj when called."""
    return Finalize(obj, func, args, kwargs)


class Finalize:
    """Callback to prevent garbage collection of an object."""
    
    def __init__(self, obj, func, args=(), kwargs=None, atexit=True):
        if kwargs is None:
            kwargs = {}
        
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.atexit = atexit
        
        if obj is None:
            self._weak = None
        else:
            def _callback(ref):
                self.func(*self.args, **self.kwargs)
            self._weak = ref(obj, _callback)
    
    def __call__(self, *args, **kwargs):
        if self._weak is not None:
            self.func(*self.args, **self.kwargs)
    
    def detach(self):
        """Return the callback and prevent further callbacks."""
        if self._weak is not None:
            self._weak = None
            return self.func
        return None
    
    def peek(self):
        """Return the callback without detaching."""
        return self.func if self._weak is not None else None
    
    def alive(self):
        """Return whether the referent is still alive."""
        return self._weak is not None and self._weak() is not None
    
    def __repr__(self):
        return f'<Finalize object at {id(self)}>'
