"""struct module for CustomPython OS.

Pack and unpack primitive data types (uses built-in _struct).
"""

from _struct import (
    Struct,
    pack,
    pack_into,
    unpack,
    unpack_from,
    calcsize,
    error,
)


def pack(fmt, *args, **kwargs):
    """Pack the values v1, v2, ... according to the format string fmt."""
    return Struct(fmt).pack(*args, **kwargs)


def pack_into(fmt, buffer, offset, *args, **kwargs):
    """Pack the values v1, v2, ... according to the format string fmt into buffer."""
    return Struct(fmt).pack_into(buffer, offset, *args, **kwargs)


def unpack(fmt, buffer):
    """Unpack from the buffer buffer (presumably packed by pack(fmt, ...)) according to the format string fmt."""
    return Struct(fmt).unpack(buffer)


def unpack_from(fmt, buffer, offset=0):
    """Unpack from the buffer buffer starting at position offset according to the format string fmt."""
    return Struct(fmt).unpack_from(buffer, offset)


def calcsize(fmt):
    """Return the size of the struct (and hence of the bytes object produced by pack(fmt, ...))."""
    return Struct(fmt).size


# Format characters
# ? - _Bool           - bool           - 1
# c - char            - bytes          - 1
# b - signed char     - int            - 1
# B - unsigned char   - int            - 1
# h - short           - int            - 2
# H - unsigned short  - int            - 2
# i - int             - int            - 4
# I - unsigned int    - int            - 4
# l - long            - int            - 4
# L - unsigned long   - int            - 4
# q - long long       - int            - 8
# Q - unsigned long long - int         - 8
# n - ssize_t         - int            - system dependent
# N - size_t          - int            - system dependent
# f - float           - float          - 4
# d - double          - float          - 8
# s - char[]          - bytes          - length
# p - char[]          - bytes          - length
# P - void*           - int            - system dependent

# Byte order, size, and alignment
# @ - native
# = - native standard
# < - little-endian
# > - big-endian
# ! - network (= big-endian)


class Struct:
    """Pack and unpack C data types."""
    
    def __init__(self, format):
        self.format = format
        self.size = calcsize(format)
    
    def pack(self, *args, **kwargs):
        return pack(self.format, *args, **kwargs)
    
    def pack_into(self, buffer, offset, *args, **kwargs):
        return pack_into(self.format, buffer, offset, *args, **kwargs)
    
    def unpack(self, buffer):
        return unpack(self.format, buffer)
    
    def unpack_from(self, buffer, offset=0):
        return unpack_from(self.format, buffer, offset)
    
    def __repr__(self):
        return f'<Struct: {self.format!r}>'


# Pack/unpack helper functions
def pack(fmt, *args, **kwargs):
    """Pack values according to format string."""
    # Simplified implementation
    result = bytearray()
    
    # Parse format string
    byte_order = '@'  # Default: native
    idx = 0
    if fmt and fmt[0] in '@=<>!':
        byte_order = fmt[0]
        idx = 1
    
    arg_idx = 0
    
    while idx < len(fmt):
        char = fmt[idx]
        idx += 1
        
        # Skip padding
        if char in ' \t\n\r':
            continue
        
        # Parse count
        count = 1
        if char.isdigit():
            count = int(char)
            if idx < len(fmt):
                char = fmt[idx]
                idx += 1
        
        # Get value
        if arg_idx >= len(args):
            raise struct.error('pack requires at least %d arguments' % (arg_idx + 1))
        value = args[arg_idx]
        arg_idx += 1
        
        # Pack based on format character
        if char == 'x':  # padding byte
            result.extend(b'\x00' * count)
        elif char in 'cbBhHiIlLqQnN':
            # Integer types
            for _ in range(count):
                result.extend(value.to_bytes(_struct_size(char), byte_order))
        elif char in 'fd':
            # Float types
            for _ in range(count):
                import struct
                result.extend(struct.pack(byte_order + char, value))
        elif char == 's':  # char array
            if isinstance(value, str):
                value = value.encode('ascii')
            result.extend(value[:count])
            result.extend(b'\x00' * (count - len(value)))
        elif char == 'p':  # pascal string
            if isinstance(value, str):
                value = value.encode('ascii')
            length = min(len(value), count - 1)
            result.append(length)
            result.extend(value[:length])
            result.extend(b'\x00' * (count - 1 - length))
        else:
            raise struct.error('bad char in struct format')
    
    return bytes(result)


def _struct_size(char):
    """Get size of struct format character."""
    sizes = {
        'b': 1, 'B': 1, '?': 1,
        'h': 2, 'H': 2,
        'i': 4, 'I': 4, 'l': 4, 'L': 4,
        'q': 8, 'Q': 8,
        'n': 8, 'N': 8,
        'f': 4, 'd': 8,
        'c': 1,
    }
    return sizes.get(char, 1)


def unpack(fmt, buffer):
    """Unpack from buffer according to format string."""
    result = []
    idx = 0
    fmt_idx = 0
    
    byte_order = '@'
    if fmt and fmt[0] in '@=<>!':
        byte_order = fmt[0]
        fmt_idx = 1
    
    while fmt_idx < len(fmt):
        char = fmt[fmt_idx]
        fmt_idx += 1
        
        if char in ' \t\n\r':
            continue
        
        count = 1
        if char.isdigit():
            count = int(char)
            if fmt_idx < len(fmt):
                char = fmt[fmt_idx]
                fmt_idx += 1
        
        if char == 'x':
            idx += count
        elif char in 'cbBhHiIlLqQnN':
            size = _struct_size(char)
            for _ in range(count):
                value = int.from_bytes(buffer[idx:idx+size], byte_order)
                result.append(value)
                idx += size
        elif char in 'fd':
            size = _struct_size(char)
            for _ in range(count):
                import struct
                value = struct.unpack(byte_order + char, buffer[idx:idx+size])[0]
                result.append(value)
                idx += size
        elif char == 's':
            result.append(buffer[idx:idx+count])
            idx += count
        elif char == 'p':
            length = buffer[idx]
            idx += 1
            result.append(buffer[idx:idx+length])
            idx += count - 1 - length
    
    return tuple(result)


def pack_into(fmt, buffer, offset, *args):
    """Pack values into buffer at offset."""
    data = pack(fmt, *args)
    buffer[offset:offset+len(data)] = data


def unpack_from(fmt, buffer, offset=0):
    """Unpack from buffer starting at offset."""
    return unpack(fmt, buffer[offset:])


def calcsize(fmt):
    """Calculate size of format string."""
    size = 0
    idx = 0
    
    # Skip byte order
    if fmt and fmt[0] in '@=<>!':
        idx = 1
    
    while idx < len(fmt):
        char = fmt[idx]
        idx += 1
        
        if char in ' \t\n\r':
            continue
        
        count = 1
        if char.isdigit():
            count = int(char)
            if idx < len(fmt):
                char = fmt[idx]
                idx += 1
        
        if char == 'x':
            size += count
        elif char in 'cbBhHiIlLqQnN':
            size += _struct_size(char) * count
        elif char in 'fd':
            size += _struct_size(char) * count
        elif char == 's':
            size += count
        elif char == 'p':
            size += count
    
    return size
