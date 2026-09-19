"""pprint module for CustomPython OS.

Data pretty printer.
"""


class PrettyPrinter:
    """Data pretty printer."""
    
    def __init__(self, indent=1, width=80, depth=None, stream=None,
                 compact=False, sort_dicts=True):
        self._indent = indent
        self._width = width
        self._depth = depth
        self._stream = stream
        self._compact = compact
        self._sort_dicts = sort_dicts
        self._depth_count = 0
    
    def pformat(self, object):
        """Format the object and return the result string."""
        return self._format(object, 0)
    
    def pprint(self, object):
        """Pretty-print the object to the stream."""
        s = self.pformat(object)
        if self._stream is not None:
            self._stream.write(s)
            self._stream.write('\n')
        else:
            print(s)
    
    def _format(self, object, indent):
        if isinstance(object, str):
            return self._format_string(object)
        elif isinstance(object, (int, float, bool, type(None))):
            return repr(object)
        elif isinstance(object, (list, tuple)):
            return self._format_sequence(object, indent)
        elif isinstance(object, dict):
            return self._format_dict(object, indent)
        elif isinstance(object, set):
            return self._format_set(object, indent)
        elif isinstance(object, frozenset):
            return self._format_frozenset(object, indent)
        else:
            return repr(object)
    
    def _format_string(self, s):
        return repr(s)
    
    def _format_sequence(self, seq, indent):
        if not seq:
            return '()' if isinstance(seq, tuple) else '[]'
        
        items = []
        for item in seq:
            items.append(self._format(item, indent + self._indent))
        
        single_line = ', '.join(items)
        if isinstance(seq, tuple):
            single_line = f'({single_line})'
        else:
            single_line = f'[{single_line}]'
        
        if len(single_line) <= self._width:
            return single_line
        
        result = []
        prefix = ' ' * indent
        if isinstance(seq, tuple):
            result.append('(')
        else:
            result.append('[')
        
        for i, item in enumerate(items):
            if i:
                result.append(',\n')
            result.append(f'{prefix}{" " * self._indent}{item}')
        
        if isinstance(seq, tuple):
            result.append('\n' + prefix + ')')
        else:
            result.append('\n' + prefix + ']')
        
        return ''.join(result)
    
    def _format_dict(self, d, indent):
        if not d:
            return '{}'
        
        items = []
        for key, value in d.items():
            key_str = self._format(key, indent + self._indent)
            value_str = self._format(value, indent + self._indent)
            items.append(f'{key_str}: {value_str}')
        
        single_line = '{' + ', '.join(items) + '}'
        if len(single_line) <= self._width:
            return single_line
        
        result = []
        prefix = ' ' * indent
        result.append('{\n')
        
        for i, item in enumerate(items):
            if i:
                result.append(',\n')
            result.append(f'{prefix}{" " * self._indent}{item}')
        
        result.append('\n' + prefix + '}')
        return ''.join(result)
    
    def _format_set(self, s, indent):
        if not s:
            return 'set()'
        
        items = []
        for item in s:
            items.append(self._format(item, indent + self._indent))
        
        single_line = '{' + ', '.join(items) + '}'
        if len(single_line) <= self._width:
            return single_line
        
        result = []
        prefix = ' ' * indent
        result.append('{\n')
        
        for i, item in enumerate(items):
            if i:
                result.append(',\n')
            result.append(f'{prefix}{" " * self._indent}{item}')
        
        result.append('\n' + prefix + '}')
        return ''.join(result)
    
    def _format_frozenset(self, fs, indent):
        if not fs:
            return 'frozenset()'
        
        items = []
        for item in fs:
            items.append(self._format(item, indent + self._indent))
        
        single_line = 'frozenset({' + ', '.join(items) + '})'
        if len(single_line) <= self._width:
            return single_line
        
        result = []
        prefix = ' ' * indent
        result.append('frozenset({\n')
        
        for i, item in enumerate(items):
            if i:
                result.append(',\n')
            result.append(f'{prefix}{" " * self._indent}{item}')
        
        result.append('\n' + prefix + '})')
        return ''.join(result)
    
    def _format(self, object, indent):
        if self._depth is not None and self._depth_count >= self._depth:
            return '...'
        
        self._depth_count += 1
        try:
            if isinstance(object, str):
                return self._format_string(object)
            elif isinstance(object, (int, float, bool, type(None))):
                return repr(object)
            elif isinstance(object, (list, tuple)):
                return self._format_sequence(object, indent)
            elif isinstance(object, dict):
                return self._format_dict(object, indent)
            elif isinstance(object, set):
                return self._format_set(object, indent)
            elif isinstance(object, frozenset):
                return self._format_frozenset(object, indent)
            else:
                return repr(object)
        finally:
            self._depth_count -= 1


def pprint(object, stream=None, indent=1, width=80, depth=None, *,
           compact=False, sort_dicts=True):
    """Pretty-print the object."""
    printer = PrettyPrinter(indent=indent, width=width, depth=depth,
                           stream=stream, compact=compact, sort_dicts=sort_dicts)
    printer.pprint(object)


def pformat(object, indent=1, width=80, depth=None, *,
            compact=False, sort_dicts=True):
    """Format the object and return the result string."""
    printer = PrettyPrinter(indent=indent, width=width, depth=depth,
                           compact=compact, sort_dicts=sort_dicts)
    return printer.pformat(object)


def pp(object, stream=None, indent=1, width=80, depth=None, *,
       compact=False, sort_dicts=True):
    """Pretty-print the object (shorthand)."""
    pprint(object, stream=stream, indent=indent, width=width, depth=depth,
           compact=compact, sort_dicts=sort_dicts)


class _safe_key:
    """Helper for sorting when the normal sort key raises TypeError."""
    
    def __init__(self, obj):
        self.obj = obj
    
    def __lt__(self, other):
        try:
            return self.obj < other.obj
        except TypeError:
            return id(self.obj) < id(other.obj)


def safesort(iterable, key=None):
    """Sort iterable, handling TypeError for incomparable elements."""
    if key is not None:
        return sorted(iterable, key=lambda x: _safe_key(key(x)))
    return sorted(iterable, key=_safe_key)
