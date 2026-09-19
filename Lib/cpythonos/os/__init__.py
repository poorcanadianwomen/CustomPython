"""os module for CustomPython OS.

Provides a portable interface to the CustomPython OS system calls.
"""

from _cpythonos import (
    read as _raw_read,
    write as _raw_write,
    open as _raw_open,
    close as _raw_close,
    getcwd as _raw_getcwd,
    chdir as _raw_chdir,
    fork as _raw_fork,
    getpid as _raw_getpid,
    getuid as _raw_getuid,
    geteuid as _raw_geteuid,
    getgid as _raw_getgid,
    getegid as _raw_getegid,
    isatty as _raw_isatty,
    strerror as _raw_strerror,
    getenv as _raw_getenv,
    urandom as _raw_urandom,
    kill as _raw_kill,
    pipe as _raw_pipe,
    dup as _raw_dup,
    dup2 as _raw_dup2,
    environ,
    error,
    O_RDONLY,
    O_WRONLY,
    O_RDWR,
    O_CREAT,
    O_EXCL,
    O_TRUNC,
    O_APPEND,
    O_NONBLOCK,
    S_ISUID,
    S_ISGID,
    S_IRUSR,
    S_IWUSR,
    S_IXUSR,
    S_IRGRP,
    S_IWGRP,
    S_IXGRP,
    S_IROTH,
    S_IWOTH,
    S_IXOTH,
    CLOCK_REALTIME,
    CLOCK_MONOTONIC,
    name,
)


# Path operations
curdir = '.'
pardir = '..'
sep = '/'
pathsep = ':'
linesep = '\n'
devnull = '/dev/null'
defpath = '/bin:/usr/bin'
altsep = None
extsep = '.'


def read(fd, count):
    """Read from a file descriptor."""
    return _raw_read(fd, count)


def write(fd, data):
    """Write to a file descriptor."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return _raw_write(fd, data)


def open(path, flags=O_RDONLY, mode=0o666):
    """Open a file."""
    if isinstance(path, str):
        path = path.encode('utf-8')
    return _raw_open(path, flags, mode)


def close(fd):
    """Close a file descriptor."""
    return _raw_close(fd)


def getcwd():
    """Get current working directory."""
    return _raw_getcwd()


def chdir(path):
    """Change working directory."""
    if isinstance(path, str):
        path = path.encode('utf-8')
    return _raw_chdir(path)


def fork():
    """Fork a child process."""
    return _raw_fork()


def getpid():
    """Get process ID."""
    return _raw_getpid()


def getppid():
    """Get parent process ID (stub)."""
    return 0


def getuid():
    """Get user ID."""
    return _raw_getuid()


def geteuid():
    """Get effective user ID."""
    return _raw_geteuid()


def getgid():
    """Get group ID."""
    return _raw_getgid()


def getegid():
    """Get effective group ID."""
    return _raw_getegid()


def isatty(fd):
    """Test if fd is a terminal."""
    return _raw_isatty(fd)


def strerror(code):
    """Get error string."""
    return _raw_strerror(code)


def getenv(key, default=None):
    """Get environment variable."""
    return _raw_getenv(key, default)


def urandom(n):
    """Get random bytes."""
    return _raw_urandom(n)


def kill(pid, sig):
    """Send signal to process."""
    return _raw_kill(pid, sig)


def pipe():
    """Create a pipe."""
    return _raw_pipe()


def dup(fd):
    """Duplicate file descriptor."""
    return _raw_dup(fd)


def dup2(old_fd, new_fd):
    """Duplicate file descriptor to specific number."""
    return _raw_dup2(old_fd, new_fd)


def listdir(path='.'):
    """List directory contents (stub)."""
    raise NotImplementedError("listdir not yet implemented for CustomPython OS")


def remove(path):
    """Remove a file (stub)."""
    raise NotImplementedError("remove not yet implemented for CustomPython OS")


def unlink(path):
    """Remove a file (alias for remove)."""
    return remove(path)


def rename(src, dst):
    """Rename a file (stub)."""
    raise NotImplementedError("rename not yet implemented for CustomPython OS")


def mkdir(path, mode=0o777):
    """Create a directory (stub)."""
    raise NotImplementedError("mkdir not yet implemented for CustomPython OS")


def rmdir(path):
    """Remove a directory (stub)."""
    raise NotImplementedError("rmdir not yet implemented for CustomPython OS")


def stat(path):
    """Get file status (stub)."""
    raise NotImplementedError("stat not yet implemented for CustomPython OS")


def chmod(path, mode):
    """Change file permissions (stub)."""
    raise NotImplementedError("chmod not yet implemented for CustomPython OS")


def getlogin():
    """Get login name."""
    return "root"


def getgroups():
    """Get group IDs."""
    return [0]


def cpu_count():
    """Return number of CPUs."""
    return 1


def get_terminal_size():
    """Get terminal size."""
    return (80, 25)


def _exit(status):
    """Exit the process."""
    import sys
    sys.exit(status)


# Path class (simplified)
class Path:
    """Simplified path operations."""
    
    def __init__(self, *parts):
        self._path = sep.join(parts) if parts else '.'
    
    def __str__(self):
        return self._path
    
    def __repr__(self):
        return f"Path('{self._path}')"
    
    def __truediv__(self, other):
        return Path(self._path, str(other))
    
    def exists(self):
        return False  # Stub
    
    def is_file(self):
        return False  # Stub
    
    def is_dir(self):
        return False  # Stub
    
    def mkdir(self, parents=False, exist_ok=False):
        raise NotImplementedError("mkdir not yet implemented")
    
    def read_text(self):
        raise NotImplementedError("read_text not yet implemented")
    
    def write_text(self, data):
        raise NotImplementedError("write_text not yet implemented")
    
    def read_bytes(self):
        raise NotImplementedError("read_bytes not yet implemented")
    
    def write_bytes(self, data):
        raise NotImplementedError("write_bytes not yet implemented")
    
    @property
    def name(self):
        return self._path.split(sep)[-1]
    
    @property
    def parent(self):
        parts = self._path.split(sep)
        return Path(*parts[:-1]) if len(parts) > 1 else Path('.')
    
    @property
    def stem(self):
        return self.name.split('.')[0] if '.' in self.name else self.name
    
    @property
    def suffix(self):
        return '.' + self.name.split('.')[-1] if '.' in self.name else ''
