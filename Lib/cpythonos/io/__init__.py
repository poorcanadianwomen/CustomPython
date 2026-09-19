"""io module for CustomPython OS.

Provides I/O operations using built-in types.
"""

import sys
from abc import ABC, abstractmethod


# Text I/O base classes
class IOBase(ABC):
    """Base class for all I/O classes."""
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
    
    @abstractmethod
    def close(self):
        self.closed = True
    
    @abstractmethod
    def fileno(self):
        raise UnsupportedOperation
    
    @abstractmethod
    def flush(self):
        pass
    
    def isatty(self):
        return False
    
    def readable(self):
        return False
    
    def readline(self, limit=-1):
        result = []
        while True:
            char = self.read(1)
            if not char or char == '\n':
                break
            result.append(char)
            if limit >= 0 and len(result) >= limit:
                break
        return ''.join(result)
    
    def readlines(self, hint=-1):
        lines = []
        total = 0
        while True:
            line = self.readline()
            if not line:
                break
            lines.append(line)
            total += len(line)
            if 0 < hint <= total:
                break
        return lines
    
    def seekable(self):
        return False
    
    def tell(self):
        raise UnsupportedOperation
    
    def writable(self):
        return False
    
    def writelines(self, lines):
        for line in lines:
            self.write(line)
    
    def seek(self, offset, whence=0):
        raise UnsupportedOperation
    
    def truncate(self, size=None):
        raise UnsupportedOperation
    
    def __iter__(self):
        return self
    
    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line
    
    def __del__(self):
        if not self.closed:
            self.close()


class RawIOBase(IOBase):
    """Base class for raw binary I/O."""
    
    @abstractmethod
    def read(self, n=-1):
        raise UnsupportedOperation
    
    @abstractmethod
    def readall(self):
        raise UnsupportedOperation
    
    @abstractmethod
    def readinto(self, b):
        raise UnsupportedOperation
    
    @abstractmethod
    def write(self, b):
        raise UnsupportedOperation


class BufferedIOBase(IOBase):
    """Base class for buffered I/O."""
    
    @abstractmethod
    def detach(self):
        raise UnsupportedOperation
    
    @abstractmethod
    def read(self, n=-1):
        raise UnsupportedOperation
    
    @abstractmethod
    def read1(self, n=-1):
        raise UnsupportedOperation
    
    @abstractmethod
    def readinto(self, b):
        raise UnsupportedOperation
    
    @abstractmethod
    def write(self, b):
        raise UnsupportedOperation


class TextIOBase(IOBase):
    """Base class for text I/O."""
    
    encoding = None
    errors = None
    newlines = None
    
    @abstractmethod
    def detach(self):
        raise UnsupportedOperation
    
    @abstractmethod
    def read(self, n=-1):
        raise UnsupportedOperation
    
    @abstractmethod
    def readline(self, limit=-1):
        raise UnsupportedOperation
    
    @abstractmethod
    def write(self, s):
        raise UnsupportedOperation


# UnsupportedOperation
class UnsupportedOperation(OSError, ValueError):
    """Unsupported operation."""
    pass


# String I/O
class StringIO(TextIOBase):
    """In-memory text stream."""
    
    def __init__(self, initial_value='', newline='\n'):
        self._buffer = initial_value
        self._pos = 0
        self._newline = newline
        self.closed = False
    
    def getvalue(self):
        return self._buffer
    
    def read(self, n=-1):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        if n < 0:
            result = self._buffer[self._pos:]
            self._pos = len(self._buffer)
        else:
            result = self._buffer[self._pos:self._pos + n]
            self._pos += n
        return result
    
    def readline(self, limit=-1):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        start = self._pos
        if limit < 0:
            end = self._buffer.find('\n', start)
            if end == -1:
                end = len(self._buffer)
            else:
                end += 1
        else:
            end = min(start + limit, len(self._buffer))
            newline_pos = self._buffer.find('\n', start, end)
            if newline_pos != -1:
                end = newline_pos + 1
        self._pos = end
        return self._buffer[start:end]
    
    def readlines(self, hint=-1):
        lines = []
        total = 0
        while True:
            line = self.readline()
            if not line:
                break
            lines.append(line)
            total += len(line)
            if 0 < hint <= total:
                break
        return lines
    
    def write(self, s):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        if not isinstance(s, str):
            raise TypeError('write() argument must be str, not ' + type(s).__name__)
        pos = self._pos
        if pos >= len(self._buffer):
            self._buffer += s
        else:
            self._buffer = self._buffer[:pos] + s + self._buffer[pos + len(s):]
        self._pos = pos + len(s)
        return len(s)
    
    def writelines(self, lines):
        for line in lines:
            self.write(line)
    
    def tell(self):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        return self._pos
    
    def seek(self, offset, whence=0):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        if whence == 0:
            self._pos = offset
        elif whence == 1:
            self._pos += offset
        elif whence == 2:
            self._pos = len(self._buffer) + offset
        else:
            raise ValueError('whence must be 0, 1 or 2')
        if self._pos < 0:
            self._pos = 0
        return self._pos
    
    def truncate(self, size=None):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        if size is None:
            size = self._pos
        if size < 0:
            raise ValueError('negative truncation size')
        self._buffer = self._buffer[:size]
        if self._pos > size:
            self._pos = size
        return size
    
    def close(self):
        self.closed = True
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
    
    def __iter__(self):
        return self
    
    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line
    
    def __repr__(self):
        return f'<StringIO {self._pos}/{len(self._buffer)}>'


# Bytes I/O
class BytesIO(BufferedIOBase):
    """In-memory binary stream."""
    
    def __init__(self, initial_bytes=b''):
        self._buffer = bytearray(initial_bytes)
        self._pos = 0
        self.closed = False
    
    def getvalue(self):
        return bytes(self._buffer)
    
    def read(self, n=-1):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        if n < 0:
            result = bytes(self._buffer[self._pos:])
            self._pos = len(self._buffer)
        else:
            result = bytes(self._buffer[self._pos:self._pos + n])
            self._pos += n
        return result
    
    def read1(self, n=-1):
        return self.read(n)
    
    def readinto(self, b):
        data = self.read(len(b))
        b[:len(data)] = data
        return len(data)
    
    def write(self, b):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        if isinstance(b, (bytes, bytearray)):
            self._buffer[self._pos:self._pos + len(b)] = b
            self._pos += len(b)
            return len(b)
        raise TypeError('write() argument must be bytes or bytearray, not ' + type(b).__name__)
    
    def tell(self):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        return self._pos
    
    def seek(self, offset, whence=0):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        if whence == 0:
            self._pos = offset
        elif whence == 1:
            self._pos += offset
        elif whence == 2:
            self._pos = len(self._buffer) + offset
        else:
            raise ValueError('whence must be 0, 1 or 2')
        if self._pos < 0:
            self._pos = 0
        return self._pos
    
    def truncate(self, size=None):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        if size is None:
            size = self._pos
        if size < 0:
            raise ValueError('negative truncation size')
        self._buffer = bytearray(self._buffer[:size])
        if self._pos > size:
            self._pos = size
        return size
    
    def readable(self):
        return True
    
    def writable(self):
        return True
    
    def seekable(self):
        return True
    
    def close(self):
        self.closed = True
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
    
    def __iter__(self):
        return self
    
    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line
    
    def __repr__(self):
        return f'<BytesIO {self._pos}/{len(self._buffer)}>'


# File I/O
class FileIO(RawIOBase):
    """File I/O using CustomPython OS syscalls."""
    
    def __init__(self, file, mode='r', closefd=True, opener=None):
        import _cpythonos
        
        self._mode = mode
        self._closefd = closefd
        self._fd = -1
        self.closed = False
        
        if isinstance(file, int):
            self._fd = file
        else:
            # Map mode to flags
            flags = 0
            if 'r' in mode:
                flags |= 0  # O_RDONLY
            elif 'w' in mode:
                flags |= 1  # O_WRONLY
                flags |= 512  # O_TRUNC
                flags |= 64  # O_CREAT
            elif 'a' in mode:
                flags |= 1  # O_WRONLY
                flags |= 1024  # O_APPEND
                flags |= 64  # O_CREAT
            
            if 'b' not in mode:
                flags |= 0  # Text mode is default
            
            self._fd = _cpythonos.open(file.encode('utf-8') if isinstance(file, str) else file, flags)
    
    def read(self, n=-1):
        import _cpythonos
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        if n < 0:
            n = 4096
        data = _cpythonos.read(self._fd, n)
        return data
    
    def readall(self):
        chunks = []
        while True:
            data = self.read(4096)
            if not data:
                break
            chunks.append(data)
        return b''.join(chunks)
    
    def readinto(self, b):
        data = self.read(len(b))
        b[:len(data)] = data
        return len(data)
    
    def write(self, b):
        import _cpythonos
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        return _cpythonos.write(self._fd, b)
    
    def fileno(self):
        return self._fd
    
    def close(self):
        import _cpythonos
        if not self.closed and self._fd >= 0:
            _cpythonos.close(self._fd)
        self.closed = True
    
    def readable(self):
        return 'r' in self._mode
    
    def writable(self):
        return 'w' in self._mode or 'a' in self._mode
    
    def seekable(self):
        return True
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


# Block I/O
class BufferedReader(BufferedIOBase):
    """Buffered reader."""
    
    def __init__(self, raw, buffer_size=8192):
        self._raw = raw
        self._buffer = bytearray()
        self._pos = 0
        self.closed = False
    
    def read(self, n=-1):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        if n < 0:
            # Read everything
            chunks = []
            while True:
                data = self._raw.read(4096)
                if not data:
                    break
                chunks.append(data)
            return b''.join(chunks)
        
        # Read from buffer first
        available = len(self._buffer) - self._pos
        if available >= n:
            result = bytes(self._buffer[self._pos:self._pos + n])
            self._pos += n
            return result
        
        # Read more from raw
        result = bytes(self._buffer[self._pos:])
        self._buffer.clear()
        self._pos = 0
        
        while len(result) < n:
            data = self._raw.read(min(4096, n - len(result)))
            if not data:
                break
            result += data
        
        return result
    
    def read1(self, n=-1):
        if n < 0:
            n = 4096
        if self._pos < len(self._buffer):
            result = bytes(self._buffer[self._pos:self._pos + n])
            self._pos += min(n, len(self._buffer) - self._pos)
            return result
        return self._raw.read(n)
    
    def write(self, b):
        return self._raw.write(b)
    
    def close(self):
        self.closed = True
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


# Text I/O wrapper
class TextIOWrapper(TextIOBase):
    """Text I/O wrapper."""
    
    def __init__(self, buffer, encoding=None, errors='strict', newline=None,
                 line_buffering=False, write_through=False):
        self._buffer = buffer
        self._encoding = encoding or 'utf-8'
        self._errors = errors
        self._newline = newline
        self._line_buffering = line_buffering
        self._write_through = write_through
        self.closed = False
    
    def read(self, n=-1):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        data = self._buffer.read(n)
        return data.decode(self._encoding)
    
    def readline(self, limit=-1):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        # Simple implementation
        result = []
        while True:
            char = self._buffer.read(1)
            if not char or char == b'\n':
                break
            result.append(char.decode(self._encoding))
            if limit >= 0 and len(result) >= limit:
                break
        return ''.join(result)
    
    def write(self, s):
        if self.closed:
            raise ValueError('I/O operation on closed file.')
        if not isinstance(s, str):
            raise TypeError('write() argument must be str, not ' + type(s).__name__)
        data = s.encode(self._encoding)
        return self._buffer.write(data)
    
    def writelines(self, lines):
        for line in lines:
            self.write(line)
    
    def close(self):
        self.closed = True
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
    
    def __iter__(self):
        return self
    
    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line


def open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None,
         closefd=True, opener=None):
    """Open a file and return a corresponding file object."""
    if isinstance(file, (str, bytes, int)):
        raw = FileIO(file, mode, closefd=closefd, opener=opener)
    else:
        raw = file
    
    if 'b' in mode:
        if buffering > 0:
            return BufferedReader(raw, buffering)
        return raw
    
    # Text mode
    if encoding is None:
        encoding = 'utf-8'
    
    wrapper = TextIOWrapper(raw, encoding=encoding, errors=errors, newline=newline)
    return wrapper
