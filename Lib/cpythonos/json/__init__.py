"""json module for CustomPython OS.

JSON encoder and decoder (built-in implementation).
"""

from _json import (
    JSONEncoder,
    JSONDecoder,
    JSONDecodeError,
    scanstring,
    dumps,
    loads,
    dump,
    load,
    decoder,
    encoder,
)


def dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True,
          allow_nan=True, cls=None, indent=None, separators=None, default=None,
          sort_keys=False, **kw):
    """Serialize obj to a JSON formatted string."""
    if cls is None:
        cls = JSONEncoder
    return cls(skipkeys=skipkeys, ensure_ascii=ensure_ascii,
               check_circular=check_circular, allow_nan=allow_nan,
               indent=indent, separators=separators, default=default,
               sort_keys=sort_keys).encode(obj)


def loads(s, cls=None, parse_float=None, parse_int=None, parse_constant=None,
          object_pairs_hook=None, **kw):
    """Deserialize s to a Python object."""
    if cls is None:
        cls = JSONDecoder
    return cls(parse_float=parse_float, parse_int=parse_int,
               parse_constant=parse_constant,
               object_pairs_hook=object_pairs_hook).decode(s)


def dump(obj, fp, *, skipkeys=False, ensure_ascii=True, check_circular=True,
         allow_nan=True, cls=None, indent=None, separators=None, default=None,
         sort_keys=False, **kw):
    """Serialize obj as a JSON formatted stream to fp."""
    for chunk in JSONEncoder(skipkeys=skipkeys, ensure_ascii=ensure_ascii,
                             check_circular=check_circular, allow_nan=allow_nan,
                             indent=indent, separators=separators, default=default,
                             sort_keys=sort_keys, **kw).iterencode(obj):
        fp.write(chunk)


def load(fp, cls=None, parse_float=None, parse_int=None, parse_constant=None,
         object_pairs_hook=None, **kw):
    """Deserialize fp to a Python object."""
    return loads(fp.read(), cls=cls, parse_float=parse_float,
                 parse_int=parse_int, parse_constant=parse_constant,
                 object_pairs_hook=object_pairs_hook, **kw)


# Alias for loads
decode = loads


class JSONDecodeError(ValueError):
    """JSON decode error."""
    
    def __init__(self, msg, doc, pos, end=None):
        super().__init__(msg)
        self.msg = msg
        self.doc = doc
        self.pos = pos
        self.end = end
    
    def __repr__(self):
        return f'JSONDecodeError({self.msg!r}, {self.doc!r}, {self.pos})'


class RawJSON:
    """Raw JSON string that won't be escaped."""
    
    def __init__(self, encoded):
        self.encoded = encoded
    
    def __repr__(self):
        return f'RawJSON({self.encoded!r})'


class JSONEncoder:
    """JSON encoder."""
    
    item_separator = ', '
    key_separator = ': '
    
    def __init__(self, *, skipkeys=False, ensure_ascii=True,
                 check_circular=True, allow_nan=True, sort_keys=False,
                 indent=None, separators=None, default=None):
        self.skipkeys = skipkeys
        self.ensure_ascii = ensure_ascii
        self.check_circular = check_circular
        self.allow_nan = allow_nan
        self.sort_keys = sort_keys
        self.indent = indent
        if separators is not None:
            self.item_separator, self.key_separator = separators
        elif indent is not None:
            self.item_separator = ',\n'
            self.key_separator = ': '
        self.default = default
    
    def encode(self, o):
        chunks = self.iterencode(o, _one_shot=True)
        if not isinstance(chunks, (list, tuple)):
            chunks = list(chunks)
        return ''.join(chunks)
    
    def iterencode(self, o, _one_shot=False):
        self._encoder = None
        self._iterencode = self._make_iterencode(o)
        return self._iterencode
    
    def _make_iterencode(self, o, markers=None, maxlevel=None, level=0,
                         _current_indent_level=None, _is_last_key=None):
        if _current_indent_level is None:
            _current_indent_level = 0
        
        indent = self.indent
        if indent is not None and not isinstance(indent, str):
            indent = ' ' * indent
        
        if isinstance(o, str):
            yield self._encode_string(o)
        elif o is None:
            yield 'null'
        elif o is True:
            yield 'true'
        elif o is False:
            yield 'false'
        elif isinstance(o, int):
            yield str(o)
        elif isinstance(o, float):
            yield self._encode_float(o)
        elif isinstance(o, (list, tuple)):
            yield from self._encode_array(o, _current_indent_level)
        elif isinstance(o, dict):
            yield from self._encode_object(o, _current_indent_level)
        elif hasattr(o, '__iter__'):
            yield from self._encode_array(list(o), _current_indent_level)
        else:
            yield from self._default(o)
    
    def _encode_string(self, s):
        if self.ensure_ascii:
            return s.encode('ascii', 'backslashreplace').decode('ascii')
        return s
    
    def _encode_float(self, o):
        if o != o:  # NaN
            if not self.allow_nan:
                raise ValueError('Out of range float values are not JSON compliant')
            return 'NaN'
        if o == float('inf'):
            if not self.allow_nan:
                raise ValueError('Out of range float values are not JSON compliant')
            return 'Infinity'
        if o == float('-inf'):
            if not self.allow_nan:
                raise ValueError('Out of range float values are not JSON compliant')
            return '-Infinity'
        return str(o)
    
    def _encode_array(self, o, _current_indent_level):
        if not o:
            return '[]'
        
        indent = self.indent
        if indent is not None:
            _current_indent_level += 1
            newline_indent = '\n' + indent * _current_indent_level
            separator = self.item_separator + newline_indent
            yield '[' + newline_indent
            for i, chunk in enumerate(o):
                if i > 0:
                    yield separator
                yield from self._make_iterencode(chunk, _current_indent_level)
            yield '\n' + indent * (_current_indent_level - 1) + ']'
        else:
            yield '[' + self.item_separator.join(
                ''.join(self._make_iterencode(chunk)) for chunk in o
            ) + ']'
    
    def _encode_object(self, o, _current_indent_level):
        if not o:
            return '{}'
        
        indent = self.indent
        if indent is not None:
            _current_indent_level += 1
            newline_indent = '\n' + indent * _current_indent_level
            separator = self.item_separator + newline_indent
            yield '{' + newline_indent
            items = sorted(o.items()) if self.sort_keys else o.items()
            for i, (key, value) in enumerate(items):
                if i > 0:
                    yield separator
                yield self._encode_string(key) + self.key_separator
                yield from self._make_iterencode(value, _current_indent_level)
            yield '\n' + indent * (_current_indent_level - 1) + '}'
        else:
            items = sorted(o.items()) if self.sort_keys else o.items()
            yield '{' + self.item_separator.join(
                self._encode_string(key) + self.key_separator +
                ''.join(self._make_iterencode(value))
                for key, value in items
            ) + '}'
    
    def _default(self, o):
        if self.default is not None:
            return self._make_iterencode(self.default(o))
        raise TypeError(f'Object of type {type(o).__name__} is not JSON serializable')


class JSONDecoder:
    """JSON decoder."""
    
    def __init__(self, *, object_hook=None, parse_float=None,
                 parse_int=None, parse_constant=None,
                 object_pairs_hook=None):
        self.object_hook = object_hook
        self.parse_float = parse_float or float
        self.parse_int = parse_int or int
        self.parse_constant = parse_constant
        self.object_pairs_hook = object_pairs_hook
    
    def decode(self, s, _w=None):
        obj, end = self.raw_decode(s)
        if end != len(s):
            raise JSONDecodeError('Extra data', s, end)
        return obj
    
    def raw_decode(self, s, idx=0):
        try:
            return _json_decode(s, idx, self)
        except JSONDecodeError as e:
            raise


def _json_decode(s, idx, decoder):
    """Internal JSON decode function."""
    # This is a simplified decoder - in production, use the C implementation
    idx = _whitespace(s, idx)
    if idx >= len(s):
        raise JSONDecodeError('Expecting value', s, idx)
    
    char = s[idx]
    if char == '{':
        return _decode_object(s, idx, decoder)
    elif char == '[':
        return _decode_array(s, idx, decoder)
    elif char == '"':
        return _decode_string(s, idx, decoder)
    elif char == 't':
        return True, idx + 4
    elif char == 'f':
        return False, idx + 5
    elif char == 'n':
        return None, idx + 4
    elif char == '-':
        return _decode_number(s, idx, decoder)
    elif char.isdigit():
        return _decode_number(s, idx, decoder)
    else:
        raise JSONDecodeError('Expecting value', s, idx)


def _whitespace(s, idx):
    """Skip whitespace."""
    while idx < len(s) and s[idx] in ' \t\n\r':
        idx += 1
    return idx


def _decode_string(s, idx, decoder):
    """Decode a JSON string."""
    idx += 1  # Skip opening quote
    result = []
    while idx < len(s):
        char = s[idx]
        if char == '"':
            return ''.join(result), idx + 1
        elif char == '\\':
            idx += 1
            escape = s[idx]
            if escape == '"': result.append('"')
            elif escape == '\\': result.append('\\')
            elif escape == '/': result.append('/')
            elif escape == 'b': result.append('\b')
            elif escape == 'f': result.append('\f')
            elif escape == 'n': result.append('\n')
            elif escape == 'r': result.append('\r')
            elif escape == 't': result.append('\t')
            elif escape == 'u':
                hex_str = s[idx+1:idx+5]
                result.append(chr(int(hex_str, 16)))
                idx += 4
        else:
            result.append(char)
        idx += 1
    raise JSONDecodeError('Unterminated string', s, idx)


def _decode_number(s, idx, decoder):
    """Decode a JSON number."""
    start = idx
    if s[idx] == '-':
        idx += 1
    while idx < len(s) and s[idx].isdigit():
        idx += 1
    if idx < len(s) and s[idx] == '.':
        idx += 1
        while idx < len(s) and s[idx].isdigit():
            idx += 1
    if idx < len(s) and s[idx] in 'eE':
        idx += 1
        if idx < len(s) and s[idx] in '+-':
            idx += 1
        while idx < len(s) and s[idx].isdigit():
            idx += 1
    
    num_str = s[start:idx]
    if '.' in num_str or 'e' in num_str or 'E' in num_str:
        return decoder.parse_float(num_str), idx
    return decoder.parse_int(num_str), idx


def _decode_array(s, idx, decoder):
    """Decode a JSON array."""
    idx += 1  # Skip opening bracket
    result = []
    idx = _whitespace(s, idx)
    if idx < len(s) and s[idx] == ']':
        return result, idx + 1
    while True:
        value, idx = _json_decode(s, idx, decoder)
        result.append(value)
        idx = _whitespace(s, idx)
        if idx >= len(s):
            raise JSONDecodeError('Expecting ',' delimiter', s, idx)
        if s[idx] == ']':
            return result, idx + 1
        if s[idx] != ',':
            raise JSONDecodeError('Expecting ',' delimiter', s, idx)
        idx += 1
        idx = _whitespace(s, idx)


def _decode_object(s, idx, decoder):
    """Decode a JSON object."""
    idx += 1  # Skip opening brace
    result = {}
    idx = _whitespace(s, idx)
    if idx < len(s) and s[idx] == '}':
        return result, idx + 1
    while True:
        idx = _whitespace(s, idx)
        if idx >= len(s) or s[idx] != '"':
            raise JSONDecodeError('Expecting property name', s, idx)
        key, idx = _decode_string(s, idx, decoder)
        idx = _whitespace(s, idx)
        if idx >= len(s) or s[idx] != ':':
            raise JSONDecodeError("Expecting ':' delimiter", s, idx)
        idx += 1
        value, idx = _json_decode(s, idx, decoder)
        result[key] = value
        idx = _whitespace(s, idx)
        if idx >= len(s):
            raise JSONDecodeError('Expecting ',' delimiter or }', s, idx)
        if s[idx] == '}':
            return result, idx + 1
        if s[idx] != ',':
            raise JSONDecodeError('Expecting ',' delimiter', s, idx)
        idx += 1
