"""collections module for CustomPython OS.

Container data types.
"""

import sys
from itertools import repeat, chain, starmap
from _collections_abc import dict_keys, dict_values, dict_items


__all__ = [
    'ChainMap', 'Counter', 'OrderedDict', 'defaultdict',
    'namedtuple', 'deque', 'UserDict', 'UserList', 'UserString',
]


def namedtuple(typename, field_names, *, rename=False, defaults=None, module=None):
    """Create a named tuple type."""
    # Use the C implementation if available
    try:
        from _collections import namedtuple as _namedtuple
        return _namedtuple(typename, field_names, rename=rename, defaults=defaults)
    except ImportError:
        pass
    
    # Pure Python implementation
    if rename:
        field_names = list(field_names)
        seen = set()
        for i, name in enumerate(field_names):
            if name.startswith('_') and not rename:
                raise ValueError(f'Field names cannot start with an underscore: {name!r}')
            if name in seen:
                name = f'_{i}'
            seen.add(name)
            field_names[i] = name
    
    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split()
    field_names = list(field_names)
    
    for name in field_names:
        if not name.isidentifier():
            raise ValueError(f'Field names must be valid identifiers: {name!r}')
        if name in ('self', 'cls', 'mcs'):
            raise ValueError(f'Field names cannot be reserved words: {name!r}')
    
    numfields = len(field_names)
    argtxt = ', '.join(field_names)
    repfmt = ', '.join(f'{name}={{{name}!r}}' for name in field_names)
    dicttxt = ', '.join(f'{name!r}: {name}' for name in field_names)
    
    if defaults is not None:
        if not isinstance(defaults, tuple):
            raise TypeError('defaults must be a tuple')
        if len(defaults) > numfields:
            raise ValueError('defaults has more items than field names')
        defaults = (None,) * (numfields - len(defaults)) + defaults
    
    template = f'''class {typename}(tuple):
    """{typename}({argtxt})"""
    
    __slots__ = ()
    
    _fields = {field_names!r}
    _field_defaults = {defaults or {}!r}
    
    def __new__(_cls, {argtxt}):
        return _tuple_new(_cls, ({argtxt},))
    
    @classmethod
    def _make(cls, iterable, new=tuple.__new__, len=len):
        return new(cls, iterable)
    
    def __repr__(self):
        return '{typename}({repfmt})'.format(**self._asdict())
    
    def _asdict(self):
        return {{{dicttxt}}}
    
    def _replace(self, /, **kwds):
        result = self._make(map(kwds.pop, {field_names!r}, self))
        if kwds:
            raise ValueError(f'got unexpected keyword arguments: {{list(kwds)!r}}')
        return result
    
    def __getnewargs__(self):
        return tuple(self)
    
    def __getstate__(self):
        return None
    
    @classmethod
    def _make(cls, iterable, new=tuple.__new__, len=len):
        result = new(cls, iterable)
        if len(result) != {numfields}:
            raise TypeError(f'Expected {numfields} arguments, got {{len(result)}}')
        return result
'''
    
    namespace = {'_tuple_new': tuple.__new__, '__name__': typename}
    try:
        exec(template, namespace)
    except SyntaxError as e:
        raise SyntaxError(e.msg, e.filename, e.lineno)
    
    result = namespace[typename]
    result._fields = tuple(field_names)
    result.__doc__ = f'{typename}({argtxt})'
    
    if module is not None:
        result.__module__ = module
    
    return result


class deque:
    """Double-ended queue."""
    
    def __init__(self, iterable=None, maxlen=None):
        self._data = list(iterable) if iterable else []
        self._maxlen = maxlen
    
    def append(self, value):
        if self._maxlen and len(self._data) >= self._maxlen:
            self._data.pop(0)
        self._data.append(value)
    
    def appendleft(self, value):
        if self._maxlen and len(self._data) >= self._maxlen:
            self._data.pop()
        self._data.insert(0, value)
    
    def pop(self):
        return self._data.pop()
    
    def popleft(self):
        return self._data.pop(0)
    
    def extend(self, iterable):
        for value in iterable:
            self.append(value)
    
    def extendleft(self, iterable):
        for value in iterable:
            self.appendleft(value)
    
    def insert(self, i, value):
        self._data.insert(i, value)
    
    def remove(self, value):
        self._data.remove(value)
    
    def clear(self):
        self._data.clear()
    
    def index(self, value, start=0, stop=None):
        return self._data.index(value, start, stop or len(self._data))
    
    def count(self, value):
        return self._data.count(value)
    
    def reverse(self):
        self._data.reverse()
    
    def rotate(self, n=1):
        if n > 0:
            for _ in range(n):
                self._data.insert(0, self._data.pop())
        elif n < 0:
            for _ in range(-n):
                self._data.append(self._data.pop(0))
    
    def copy(self):
        return deque(self._data)
    
    def __len__(self):
        return len(self._data)
    
    def __getitem__(self, index):
        return self._data[index]
    
    def __setitem__(self, index, value):
        self._data[index] = value
    
    def __delitem__(self, index):
        del self._data[index]
    
    def __contains__(self, value):
        return value in self._data
    
    def __iter__(self):
        return iter(self._data)
    
    def __reversed__(self):
        return reversed(self._data)
    
    def __bool__(self):
        return bool(self._data)
    
    def __repr__(self):
        return f'deque({self._data})'
    
    def __eq__(self, other):
        if isinstance(other, deque):
            return self._data == other._data
        return NotImplemented
    
    def __hash__(self):
        raise TypeError(f'unhashable type: {type(self).__name__}')


class defaultdict(dict):
    """Dictionary with default factory for missing keys."""
    
    def __init__(self, default_factory=None, *args, **kwargs):
        if default_factory is not None and not callable(default_factory):
            raise TypeError('first argument must be callable or None')
        super().__init__(*args, **kwargs)
        self.default_factory = default_factory
    
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        value = self.default_factory()
        self[key] = value
        return value
    
    def __repr__(self):
        if self.default_factory is None:
            name = type(self).__name__
        else:
            name = f'{type(self).__name__}({self.default_factory!r})'
        return f'{name}({dict.__repr__(self)})'
    
    def copy(self):
        return type(self)(self.default_factory, self)
    
    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = (self.default_factory,)
        return type(self), args, None, None, iter(self.items())


class OrderedDict(dict):
    """Dictionary that remembers insertion order."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._order = list(self.keys())
    
    def __setitem__(self, key, value):
        if key not in self:
            self._order.append(key)
        super().__setitem__(key, value)
    
    def __delitem__(self, key):
        super().__delitem__(key)
        self._order.remove(key)
    
    def __iter__(self):
        return iter(self._order)
    
    def __reversed__(self):
        return reversed(self._order)
    
    def popitem(self, last=True):
        if not self:
            raise KeyError('dictionary is empty')
        key = self._order[-1] if last else self._order[0]
        value = super().pop(key)
        self._order.remove(key)
        return key, value
    
    def move_to_end(self, key, last=True):
        if key not in self:
            raise KeyError(key)
        self._order.remove(key)
        if last:
            self._order.append(key)
        else:
            self._order.insert(0, key)
    
    def copy(self):
        return type(self)(self)
    
    def __repr__(self):
        items = ', '.join(f'{k!r}: {v!r}' for k, v in self.items())
        return f'{{{items}}}'


class Counter(dict):
    """Counting dictionary."""
    
    def __init__(self, iterable=None, /, **kwds):
        super().__init__()
        self.update(iterable, **kwds)
    
    def __missing__(self, key):
        return 0
    
    def most_common(self, n=None):
        if n is None:
            return sorted(self.items(), key=lambda x: x[1], reverse=True)
        return sorted(self.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def elements(self):
        for elem, count in self.items():
            for _ in range(count):
                yield elem
    
    @classmethod
    def fromkeys(cls, iterable, v=0):
        c = cls()
        for elem in iterable:
            c[elem] = v
        return c
    
    def update(self, iterable=None, /, **kwds):
        if iterable is not None:
            if isinstance(iterable, dict):
                for elem, count in iterable.items():
                    self[elem] = self.get(elem, 0) + count
            else:
                for elem in iterable:
                    self[elem] = self.get(elem, 0) + 1
        if kwds:
            for elem, count in kwds.items():
                self[elem] = self.get(elem, 0) + count
    
    def subtract(self, iterable=None, /, **kwds):
        if iterable is not None:
            if isinstance(iterable, dict):
                for elem, count in iterable.items():
                    self[elem] = self.get(elem, 0) - count
            else:
                for elem in iterable:
                    self[elem] = self.get(elem, 0) - 1
        if kwds:
            for elem, count in kwds.items():
                self[elem] = self.get(elem, 0) - count
    
    def __add__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            newcount = count + other.get(elem, 0)
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return result
    
    def __sub__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            newcount = count - other.get(elem, 0)
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count < 0:
                result[elem] = -count
        return result
    
    def __or__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            newcount = max(count, other.get(elem, 0))
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return result
    
    def __and__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            newcount = min(count, other.get(elem, 0))
            if newcount > 0:
                result[elem] = newcount
        return result
    
    def __neg__(self):
        result = Counter()
        for elem, count in self.items():
            if count != 0:
                result[elem] = -count
        return result
    
    def __repr__(self):
        items = ', '.join(f'{elem!r}: {count}' for elem, count in self.items())
        return f'Counter({{{items}}})'


class ChainMap(dict):
    """Chain multiple dictionaries."""
    
    def __init__(self, *maps):
        self.maps = list(maps) or [{}]
    
    def __getitem__(self, key):
        for mapping in self.maps:
            try:
                return mapping[key]
            except KeyError:
                pass
        return self.__missing__(key)
    
    def __missing__(self, key):
        raise KeyError(key)
    
    def __contains__(self, key):
        return any(key in m for m in self.maps)
    
    def __iter__(self):
        d = {}
        for mapping in reversed(self.maps):
            d.update(mapping)
        return iter(d)
    
    def __len__(self):
        return len(set().union(*self.maps))
    
    def __bool__(self):
        return any(self.maps)
    
    def __repr__(self):
        return f'ChainMap({", ".join(repr(m) for m in self.maps)})'
    
    def copy(self):
        return type(self)(*self.maps)
    
    def new_child(self, m=None, **kwargs):
        if m is None:
            m = kwargs
        return type(self)(m, *self.maps)
    
    @property
    def maps(self):
        return self._maps
    
    @maps.setter
    def maps(self, value):
        self._maps = list(value)
    
    def __setitem__(self, key, value):
        self.maps[0][key] = value
    
    def __delitem__(self, key):
        del self.maps[0][key]
    
    def popitem(self):
        try:
            return self.maps[0].popitem()
        except KeyError:
            pass
        if len(self.maps) == 1:
            raise
        return self.maps[1].popitem()
    
    def pop(self, key, *args):
        try:
            return self.maps[0].pop(key, *args)
        except KeyError:
            if len(self.maps) == 1:
                raise
        return self.maps[1].pop(key, *args)
    
    def clear(self):
        self.maps[0].clear()


class UserDict:
    """Mutable mapping that wraps a dict."""
    
    def __init__(self, dict=None, /, **kwargs):
        self.data = dict or {}
        if kwargs:
            self.data.update(kwargs)
    
    def __contains__(self, key):
        return key in self.data
    
    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        raise KeyError(key)
    
    def __setitem__(self, key, item):
        self.data[key] = item
    
    def __delitem__(self, key):
        del self.data[key]
    
    def __iter__(self):
        return iter(self.data)
    
    def __len__(self):
        return len(self.data)
    
    def __repr__(self):
        return f'{type(self).__name__}({self.data!r})'
    
    def __eq__(self, other):
        if isinstance(other, UserDict):
            return self.data == other.data
        return self.data == other
    
    def __copy__(self):
        import copy
        return type(self)(copy.copy(self.data))
    
    def copy(self):
        return type(self)(self.data.copy())
    
    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def items(self):
        return self.data.items()
    
    def keys(self):
        return self.data.keys()
    
    def values(self):
        return self.data.values()
    
    def update(self, dict=None, **kwargs):
        if dict is not None:
            self.data.update(dict)
        if kwargs:
            self.data.update(kwargs)
    
    def pop(self, key, *args):
        return self.data.pop(key, *args)
    
    def popitem(self):
        return self.data.popitem()
    
    def setdefault(self, key, default=None):
        return self.data.setdefault(key, default)
    
    def clear(self):
        self.data.clear()


class UserList:
    """Mutable sequence that wraps a list."""
    
    def __init__(self, initlist=None):
        self.data = list(initlist) if initlist is not None else []
    
    def __contains__(self, item):
        return item in self.data
    
    def __getitem__(self, i):
        return self.data[i]
    
    def __setitem__(self, i, item):
        self.data[i] = item
    
    def __delitem__(self, i):
        del self.data[i]
    
    def __len__(self):
        return len(self.data)
    
    def __add__(self, other):
        return type(self)(self.data + list(other))
    
    def __radd__(self, other):
        return type(self)(list(other) + self.data)
    
    def __iadd__(self, other):
        self.data.extend(other)
        return self
    
    def __mul__(self, n):
        return type(self)(self.data * n)
    
    def __imul__(self, n):
        self.data *= n
        return self
    
    def __repr__(self):
        return f'{type(self).__name__}({self.data!r})'
    
    def __lt__(self, other):
        return self.data < list(other)
    
    def __le__(self, other):
        return self.data <= list(other)
    
    def __eq__(self, other):
        return self.data == list(other)
    
    def __ne__(self, other):
        return self.data != list(other)
    
    def __gt__(self, other):
        return self.data > list(other)
    
    def __ge__(self, other):
        return self.data >= list(other)
    
    def __contains__(self, item):
        return item in self.data
    
    def __iter__(self):
        return iter(self.data)
    
    def __reversed__(self):
        return reversed(self.data)
    
    def append(self, item):
        self.data.append(item)
    
    def insert(self, i, item):
        self.data.insert(i, item)
    
    def pop(self, i=-1):
        return self.data.pop(i)
    
    def remove(self, item):
        self.data.remove(item)
    
    def clear(self):
        self.data.clear()
    
    def copy(self):
        return type(self)(self.data.copy())
    
    def count(self, item):
        return self.data.count(item)
    
    def index(self, item, *args):
        return self.data.index(item, *args)
    
    def reverse(self):
        self.data.reverse()
    
    def sort(self, /, *args, **kwargs):
        self.data.sort(*args, **kwargs)
    
    def extend(self, other):
        self.data.extend(other)


class UserString:
    """Mutable string wrapper."""
    
    def __init__(self, data):
        self.data = str(data)
    
    def __str__(self):
        return self.data
    
    def __repr__(self):
        return f'{type(self).__name__}({self.data!r})'
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, i):
        return self.data[i]
    
    def __contains__(self, item):
        return item in self.data
    
    def __add__(self, other):
        if isinstance(other, UserString):
            return type(self)(self.data + other.data)
        return type(self)(self.data + str(other))
    
    def __radd__(self, other):
        return type(self)(str(other) + self.data)
    
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        else:
            self.data += str(other)
        return self
    
    def __mul__(self, n):
        return type(self)(self.data * n)
    
    def __mod__(self, args):
        return type(self)(self.data % args)
    
    def __eq__(self, other):
        if isinstance(other, UserString):
            return self.data == other.data
        return self.data == str(other)
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if isinstance(other, UserString):
            return self.data < other.data
        return self.data < str(other)
    
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other):
        if isinstance(other, UserString):
            return self.data > other.data
        return self.data > str(other)
    
    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)
    
    def __iter__(self):
        return iter(self.data)
    
    def capitalize(self):
        return type(self)(self.data.capitalize())
    
    def casefold(self):
        return type(self)(self.data.casefold())
    
    def center(self, width, *args):
        return type(self)(self.data.center(width, *args))
    
    def count(self, sub, start=0, end=None):
        return self.data.count(sub, start, end)
    
    def encode(self, encoding='utf-8', errors='strict'):
        return self.data.encode(encoding, errors)
    
    def endswith(self, suffix, start=0, end=None):
        return self.data.endswith(suffix, start, end)
    
    def expandtabs(self, tabsize=8):
        return type(self)(self.data.expandtabs(tabsize))
    
    def find(self, sub, start=0, end=None):
        return self.data.find(sub, start, end)
    
    def format(self, *args, **kwargs):
        return type(self)(self.data.format(*args, **kwargs))
    
    def format_map(self, mapping):
        return type(self)(self.data.format_map(mapping))
    
    def index(self, sub, start=0, end=None):
        return self.data.index(sub, start, end)
    
    def isalnum(self):
        return self.data.isalnum()
    
    def isalpha(self):
        return self.data.isalpha()
    
    def isascii(self):
        return self.data.isascii()
    
    def isdecimal(self):
        return self.data.isdecimal()
    
    def isdigit(self):
        return self.data.isdigit()
    
    def isidentifier(self):
        return self.data.isidentifier()
    
    def islower(self):
        return self.data.islower()
    
    def isnumeric(self):
        return self.data.isnumeric()
    
    def isprintable(self):
        return self.data.isprintable()
    
    def isspace(self):
        return self.data.isspace()
    
    def istitle(self):
        return self.data.istitle()
    
    def isupper(self):
        return self.data.isupper()
    
    def join(self, seq):
        return type(self)(self.data.join(seq))
    
    def ljust(self, width, *args):
        return type(self)(self.data.ljust(width, *args))
    
    def lower(self):
        return type(self)(self.data.lower())
    
    def lstrip(self, chars=None):
        return type(self)(self.data.lstrip(chars))
    
    def maketrans(self, *args):
        return self.data.maketrans(*args)
    
    def partition(self, sep):
        return self.data.partition(sep)
    
    def removeprefix(self, prefix):
        return type(self)(self.data.removeprefix(prefix))
    
    def removesuffix(self, suffix):
        return type(self)(self.data.removesuffix(suffix))
    
    def replace(self, old, new, count=-1):
        return type(self)(self.data.replace(old, new, count))
    
    def rfind(self, sub, start=0, end=None):
        return self.data.rfind(sub, start, end)
    
    def rindex(self, sub, start=0, end=None):
        return self.data.rindex(sub, start, end)
    
    def rjust(self, width, *args):
        return type(self)(self.data.rjust(width, *args))
    
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    
    def rstrip(self, chars=None):
        return type(self)(self.data.rstrip(chars))
    
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    
    def splitlines(self, keepends=False):
        return self.data.splitlines(keepends)
    
    def startswith(self, prefix, start=0, end=None):
        return self.data.startswith(prefix, start, end)
    
    def strip(self, chars=None):
        return type(self)(self.data.strip(chars))
    
    def swapcase(self):
        return type(self)(self.data.swapcase())
    
    def title(self):
        return type(self)(self.data.title())
    
    def translate(self, *args):
        return type(self)(self.data.translate(*args))
    
    def upper(self):
        return type(self)(self.data.upper())
    
    def zfill(self, width):
        return type(self)(self.data.zfill(width))
