"""base64 module for CustomPython OS.

Base16, Base32, Base64, Base85 Data Encodings.
"""

import sys


# Base64 encoding/decoding tables
_B64CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
_B64ALTCHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
_B32CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
_B16CHARS = '0123456789ABCDEF'


def b64encode(s, altchars=None, validate=True):
    """Encode bytes-like object s using Base64 and return a bytes object."""
    if not isinstance(s, (bytes, bytearray)):
        raise TypeError('expected bytes-like object, not %s' % type(s).__name__)
    
    if validate and not s:
        return b''
    
    result = []
    for i in range(0, len(s), 3):
        chunk = s[i:i+3]
        # Convert to 24-bit number
        n = int.from_bytes(chunk, 'big')
        # Pad if needed
        padding = 3 - len(chunk)
        n <<= padding * 8
        
        # Extract 6-bit groups
        for j in range(4):
            if j < 4 - padding:
                idx = (n >> (18 - j * 6)) & 0x3F
                result.append(_B64CHARS[idx])
            else:
                result.append('=')
    
    encoded = ''.join(result)
    if altchars is not None:
        if len(altchars) != 2:
            raise ValueError('altchars must be of length 2')
        table = str.maketrans(_B64CHARS[:64], altchars[:2] * 32)
        encoded = encoded.translate(table)
    
    return encoded.encode('ascii')


def b64decode(s, altchars=None, validate=True):
    """Decode Base64 encoded bytes."""
    if isinstance(s, str):
        s = s.encode('ascii')
    
    if not isinstance(s, (bytes, bytearray)):
        raise TypeError('expected bytes-like object, not %s' % type(s).__name__)
    
    # Remove whitespace
    s = bytes(c for c in s if c not in b' \t\n\r')
    
    # Handle altchars
    if altchars is not None:
        if len(altchars) != 2:
            raise ValueError('altchars must be of length 2')
        table = bytes.maketrans(altchars[:2] * 32, _B64CHARS[:64] * 2)
        s = s.translate(table)
    
    # Add padding if needed
    padding = 4 - (len(s) % 4)
    if padding != 4:
        s += b'=' * padding
    
    result = []
    for i in range(0, len(s), 4):
        chunk = s[i:i+4]
        if chunk == b'====':
            continue
        
        # Convert 4 base64 characters to 3 bytes
        n = 0
        for j, c in enumerate(chunk):
            if c == ord('='):
                n <<= 6
            else:
                idx = _B64CHARS.index(chr(c))
                n = (n << 6) | idx
        
        # Extract bytes
        padding_count = chunk.count(b'=')
        for j in range(3 - padding_count):
            result.append((n >> (16 - j * 8)) & 0xFF)
    
    return bytes(result)


def b32encode(s):
    """Encode bytes-like object s using Base32 and return a bytes object."""
    if not isinstance(s, (bytes, bytearray)):
        raise TypeError('expected bytes-like object, not %s' % type(s).__name__)
    
    result = []
    for i in range(0, len(s), 5):
        chunk = s[i:i+5]
        n = int.from_bytes(chunk, 'big')
        padding = 5 - len(chunk)
        n <<= padding * 8
        
        for j in range(8):
            if j < 8 - padding:
                idx = (n >> (35 - j * 5)) & 0x1F
                result.append(_B32CHARS[idx])
            else:
                result.append('=')
    
    return ''.join(result).encode('ascii')


def b32decode(s, casefold=False, map01=None):
    """Decode Base32 encoded bytes."""
    if isinstance(s, str):
        s = s.encode('ascii')
    
    s = bytes(c for c in s if c not in b' \t\n\r')
    
    if casefold:
        s = s.upper()
    
    if map01 is not None:
        s = s.replace(b'1', map01.encode() if isinstance(map01, str) else map01)
    
    # Add padding
    padding = 8 - (len(s) % 8)
    if padding != 8:
        s += b'=' * padding
    
    result = []
    for i in range(0, len(s), 8):
        chunk = s[i:i+8]
        n = 0
        for j, c in enumerate(chunk):
            if c == ord('='):
                n <<= 5
            else:
                idx = _B32CHARS.index(chr(c))
                n = (n << 5) | idx
        
        padding_count = chunk.count(b'=')
        for j in range(5 - padding_count):
            result.append((n >> (32 - j * 8)) & 0xFF)
    
    return bytes(result)


def b16encode(s):
    """Encode bytes-like object s using Base16 and return a bytes object."""
    return s.hex().upper().encode('ascii')


def b16decode(s, casefold=False):
    """Decode Base16 encoded bytes."""
    if isinstance(s, str):
        s = s.encode('ascii')
    
    if casefold:
        s = s.upper()
    
    # Remove whitespace
    s = bytes(c for c in s if c not in b' \t\n\r')
    
    return bytes.fromhex(s.decode('ascii'))


def b85encode(s, alpha=True, adobe=False):
    """Encode bytes-like object s using Base85 and return a bytes object."""
    if not isinstance(s, (bytes, bytearray)):
        raise TypeError('expected bytes-like object, not %s' % type(s).__name__)
    
    result = []
    for i in range(0, len(s), 4):
        chunk = s[i:i+4]
        n = int.from_bytes(chunk, 'big')
        
        # Encode 5 characters
        for j in range(5):
            n, remainder = divmod(n, 85)
            if alpha:
                result.append(chr(remainder + 33))
            else:
                result.append(chr(remainder + 33))
        
        # Remove leading '!' for non-alpha
        if not alpha:
            result[-5:] = reversed(result[-5:])
    
    return ''.join(result).encode('ascii')


def b85decode(s, alpha=True, adobe=False):
    """Decode Base85 encoded bytes."""
    if isinstance(s, str):
        s = s.encode('ascii')
    
    # Remove adobe markers
    if adobe:
        s = s.replace(b'<~', b'').replace(b'~>', b'')
    
    result = []
    for i in range(0, len(s), 5):
        chunk = s[i:i+5]
        n = 0
        for j, c in enumerate(chunk):
            n = n * 85 + (c - 33)
        
        for j in range(4):
            result.append((n >> (24 - j * 8)) & 0xFF)
    
    return bytes(result)


def urlsafe_b64encode(s):
    """Encode bytes-like object s using the URL- and filesystem-safe Base64 alphabet."""
    return b64encode(s, altchars=b'-_')


def urlsafe_b64decode(s):
    """Decode bytes-like object or ASCII string s using the URL- and filesystem-safe Base64 alphabet."""
    return b64decode(s, altchars=b'-_')


def encodebytes(s):
    """Encode bytes-like object s using Base64 and return a bytes object (with newlines)."""
    result = b64encode(s)
    return b'\n'.join(result[i:i+76] for i in range(0, len(result), 76)) + b'\n'


def decodebytes(s):
    """Decode bytes-like object or ASCII string s using Base64 and return bytes."""
    return b64decode(s)


def decodeascii(s):
    """Decode ASCII string s using Base64 and return bytes."""
    if isinstance(s, str):
        s = s.encode('ascii')
    return b64decode(s)


# Standard aliases
encode = encodebytes
decode = decodebytes
