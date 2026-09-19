"""threading module for CustomPython OS.

Provides threading support using CustomPython OS syscalls.
"""

import _cpythonos

# Thread-related exceptions
class ThreadError(Exception):
    """Thread-related error."""
    pass


class error(ThreadError):
    """Thread-related error (alias)."""
    pass


# Constants
ACTIVE_NON_DAEMON_COUNT = 0

# Thread local storage
class local:
    """Thread-local data."""
    
    def __init__(self):
        self._dict = {}
    
    def __getattr__(self, name):
        if name in self._dict:
            return self._dict[name]
        raise AttributeError(f"'local' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        if name == '_dict':
            super().__setattr__(name, value)
        else:
            self._dict[name] = value
    
    def __delattr__(self, name):
        if name in self._dict:
            del self._dict[name]
        else:
            raise AttributeError(f"'local' object has no attribute '{name}'")


class Thread:
    """A thread of execution."""
    
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None,
                 daemon=None):
        self._target = target
        self._name = name or f"Thread-{id(self)}"
        self._args = args
        self._kwargs = kwargs or {}
        self._daemon = daemon
        self._started = False
        self._is_stopped = False
        self._ident = None
        
        if daemon is None:
            self._daemon = False
    
    def start(self):
        """Start the thread."""
        if self._started:
            raise RuntimeError("Thread already started")
        
        # TODO: Implement actual thread creation via syscalls
        self._started = True
        self._ident = id(self)
        
        # For now, just run the target function directly
        if self._target:
            self._target(*self._args, **self._kwargs)
    
    def run(self):
        """Run the thread."""
        if self._target:
            self._target(*self._args, **self._kwargs)
    
    def join(self, timeout=None):
        """Wait for the thread to finish."""
        # Stub - needs actual implementation
        pass
    
    def is_alive(self):
        """Return whether the thread is alive."""
        return self._started and not self._is_stopped
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def ident(self):
        return self._ident
    
    @property
    def daemon(self):
        return self._daemon
    
    @daemon.setter
    def daemon(self, value):
        if self._started:
            raise RuntimeError("Cannot set daemon status of active thread")
        self._daemon = value
    
    def setDaemon(self, daemonic):
        """Set daemon status (deprecated, use daemon property)."""
        self.daemon = daemonic
    
    def isDaemon(self):
        """Return daemon status (deprecated, use daemon property)."""
        return self.daemon
    
    def getName(self):
        """Return thread name (deprecated, use name property)."""
        return self.name
    
    def setName(self, name):
        """Set thread name (deprecated, use name property)."""
        self.name = name


class Timer(Thread):
    """Call a function after a specified number of seconds."""
    
    def __init__(self, interval, function, args=None, kwargs=None):
        super().__init__()
        self._interval = interval
        self._function = function
        self._args = args or ()
        self._kwargs = kwargs or {}
        self._finished = False
        self._cancel = False
    
    def run(self):
        import time
        time.sleep(self._interval)
        if not self._cancel:
            self._function(*self._args, **self._kwargs)
        self._finished = True
    
    def cancel(self):
        """Cancel the timer."""
        self._cancel = True
    
    def is_alive(self):
        """Return whether the timer is still running."""
        return not self._finished


class Event:
    """A thread-safe event flag."""
    
    def __init__(self):
        self._flag = False
    
    def set(self):
        """Set the event flag."""
        self._flag = True
    
    def clear(self):
        """Clear the event flag."""
        self._flag = False
    
    def wait(self, timeout=None):
        """Wait for the event flag to be set."""
        import time
        if timeout is None:
            while not self._flag:
                time.sleep(0.01)
            return True
        else:
            start = time.monotonic()
            while not self._flag:
                if time.monotonic() - start >= timeout:
                    return False
                time.sleep(0.01)
            return True
    
    def is_set(self):
        """Return whether the event flag is set."""
        return self._flag
    
    isSet = is_set


class Lock:
    """A mutex lock."""
    
    def __init__(self):
        self._locked = False
    
    def acquire(self, blocking=True, timeout=-1):
        """Acquire the lock."""
        if blocking:
            import time
            start = time.monotonic()
            while self._locked:
                if timeout >= 0:
                    if time.monotonic() - start >= timeout:
                        return False
                time.sleep(0.01)
            self._locked = True
            return True
        else:
            if self._locked:
                return False
            self._locked = True
            return True
    
    def release(self):
        """Release the lock."""
        if not self._locked:
            raise RuntimeError("release unlocked lock")
        self._locked = False
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False
    
    def locked(self):
        """Return whether the lock is locked."""
        return self._locked


class RLock:
    """A reentrant mutex lock."""
    
    def __init__(self):
        self._lock = Lock()
        self._count = 0
        self._owner = None
    
    def acquire(self, blocking=True, timeout=-1):
        """Acquire the lock."""
        me = id(self._get_current_thread())
        if self._owner == me:
            self._count += 1
            return True
        if self._lock.acquire(blocking, timeout):
            self._owner = me
            self._count = 1
            return True
        return False
    
    def release(self):
        """Release the lock."""
        if self._owner != id(self._get_current_thread()):
            raise RuntimeError("release unlocked lock")
        self._count -= 1
        if self._count == 0:
            self._owner = None
            self._lock.release()
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False
    
    def _get_current_thread(self):
        """Get current thread (stub)."""
        return None


class Condition:
    """Condition variable."""
    
    def __init__(self, lock=None):
        self._lock = lock or Lock()
        self._waiters = []
    
    def acquire(self, *args):
        """Acquire the underlying lock."""
        return self._lock.acquire(*args)
    
    def release(self):
        """Release the underlying lock."""
        self._lock.release()
    
    def wait(self, timeout=None):
        """Wait until notified or timeout."""
        # Stub - needs actual implementation
        import time
        if timeout:
            time.sleep(timeout)
        return True
    
    def wait_for(self, predicate, timeout=None):
        """Wait until predicate returns true."""
        result = predicate()
        while not result:
            self.wait(timeout)
            result = predicate()
        return result
    
    def notify(self, n=1):
        """Wake up n threads waiting on this condition."""
        pass
    
    def notify_all(self):
        """Wake up all threads waiting on this condition."""
        pass
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False


class Semaphore:
    """A semaphore object."""
    
    def __init__(self, value=1):
        if value < 0:
            raise ValueError("semaphore initial value must be >= 0")
        self._value = value
        self._lock = Lock()
    
    def acquire(self, blocking=True, timeout=-1):
        """Acquire the semaphore."""
        if self._value > 0:
            self._value -= 1
            return True
        if not blocking:
            return False
        # Stub - needs actual implementation
        import time
        time.sleep(0.01)
        self._value -= 1
        return True
    
    def release(self):
        """Release the semaphore."""
        self._value += 1
    
    def __enter__(self):
        self.acquire()
        return self
    
    class BoundedSemaphore(Semaphore):
        """A bounded semaphore."""
        
        def release(self):
            if self._value >= self._initial_value:
                raise ValueError("BoundedSemaphore released too many times")
            super().release()


# Module-level functions
def current_thread():
    """Return the current Thread object."""
    return Thread(name="MainThread")


def active_count():
    """Return the number of Thread objects that are active."""
    return 1


def enumerate():
    """Return a list of all active Thread objects."""
    return [current_thread()]


def main_thread():
    """Return the main Thread object."""
    return Thread(name="MainThread")


def stack_size(size=0):
    """Set or return the thread stack size."""
    return 0


def get_ident():
    """Return a non-zero integer that is unique for the current thread."""
    return id(current_thread())


def get_native_id():
    """Return a non-negative integer identifying the current thread."""
    return get_ident()
