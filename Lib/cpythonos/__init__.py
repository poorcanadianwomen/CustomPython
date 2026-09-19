# CustomPython OS Python Init
# __init__.py for the cpythonos package

"""
CustomPython OS interface module.

This module provides Python bindings for the CustomPython OS system calls.
"""

import _cpythonos

# Import all public functions
from _cpythonos import (
    read,
    write,
    open,
    close,
    fstat,
    getcwd,
    chdir,
    fork,
    execve,
    waitpid,
    getpid,
    getuid,
    geteuid,
    getgid,
    getegid,
    isatty,
    strerror,
    getenv,
    urandom,
    kill,
    pipe,
    dup,
    dup2,
)

# Export environ
environ = _cpythonos.environ

# Constants
O_RDONLY = 0
O_WRONLY = 1
O_RDWR = 2
O_CREAT = 64
O_EXCL = 128
O_TRUNC = 512
O_APPEND = 1024
O_NONBLOCK = 2048

# File permission bits
S_ISUID = 0o4000
S_ISGID = 0o2000
S_IRUSR = 0o400
S_IWUSR = 0o200
S_IXUSR = 0o100
S_IRGRP = 0o040
S_IWGRP = 0o020
S_IXGRP = 0o010
S_IROTH = 0o004
S_IWOTH = 0o002
S_IXOTH = 0o001

# Clock IDs
CLOCK_REALTIME = 0
CLOCK_MONOTONIC = 1

# Name
name = "custompython"

# Path operations
path = None  # Will be populated by posixpath or ntpath

# Error handling
error = OSError

def listdir(path='.'):
    """List directory contents (stub - needs filesystem support)."""
    raise NotImplementedError("listdir not yet implemented")

def remove(path):
    """Remove a file (stub - needs filesystem support)."""
    raise NotImplementedError("remove not yet implemented")

def rename(src, dst):
    """Rename a file (stub - needs filesystem support)."""
    raise NotImplementedError("rename not yet implemented")

def mkdir(path, mode=0o777):
    """Create a directory (stub - needs filesystem support)."""
    raise NotImplementedError("mkdir not yet implemented")

def rmdir(path):
    """Remove a directory (stub - needs filesystem support)."""
    raise NotImplementedError("rmdir not yet implemented")

def stat(path):
    """Get file status (stub - needs filesystem support)."""
    raise NotImplementedError("stat not yet implemented")

def chmod(path, mode):
    """Change file permissions (stub - needs filesystem support)."""
    raise NotImplementedError("chmod not yet implemented")

def getlogin():
    """Get login name (stub)."""
    return "root"

def getgroups():
    """Get group IDs (stub)."""
    return [0]

def setuid(uid):
    """Set user ID (stub)."""
    raise NotImplementedError("setuid not yet implemented")

def setgid(gid):
    """Set group ID (stub)."""
    raise NotImplementedError("setgid not yet implemented")

def cpu_count():
    """Return number of CPUs."""
    return 1

def get_terminal_size():
    """Get terminal size."""
    return (80, 25)
