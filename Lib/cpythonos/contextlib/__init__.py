"""contextlib module for CustomPython OS.

Context manager utilities.
"""


class ContextDecorator:
    """A base class or mixin that enables context managers to work as decorators."""
    
    def _recreate_cm(self):
        """Return a recreated instance of self."""
        return self
    
    def __call__(self, func):
        def inner(*args, **kwds):
            with self._recreate_cm():
                return func(*args, **kwds)
        return inner


class ExitStack:
    """Context manager for dynamically managing a stack of context managers."""
    
    def __init__(self):
        self._exit_callbacks = []
    
    def push(self, exit):
        """Registers a callback with the standard __exit__ method signature."""
        def _exit_wrapper(exc_type, exc_val, exc_tb):
            return exit(exc_type, exc_val, exc_tb)
        _exit_wrapper.__self__ = exit
        self._exit_callbacks.append(_exit_wrapper)
        return exit
    
    def push_exit_callback(self, exit, is_sync=True):
        """Registers an arbitrary callback with the standard __exit__ method."""
        def _exit_wrapper(exc_type, exc_val, exc_tb):
            return exit(exc_type, exc_val, exc_tb)
        self._exit_callbacks.append(_exit_wrapper)
        return _exit_wrapper
    
    def __enter__(self):
        return self
    
    def __exit__(self, *exc_details):
        received_exc = exc_details[0] is not None
        exc = exc_details
        suppressed_exc = False
        
        while self._exit_callbacks:
            exit_func = self._exit_callbacks.pop()
            try:
                if exit_func(*exc):
                    suppressed_exc = True
                    exc = (None, None, None)
            except:
                exc = sys.exc_info()
        
        return received_exc and suppressed_exc
    
    def callback(self, func, *args, **kwds):
        """Registers a arbitrary callback with the standard __exit__ method."""
        def _exit_wrapper(exc_type, exc_val, exc_tb):
            func(*args, **kwds)
        self._exit_callbacks.append(_exit_wrapper)
        return func
    
    def enter_context(self, cm):
        """Enters an arbitrary context manager."""
        result = cm.__enter__()
        self.push(cm)
        return result
    
    def close(self):
        """Immediately unregister all existing context managers."""
        self.__exit__(None, None, None)


class AsyncExitStack:
    """Async context manager for dynamically managing a stack of context managers."""
    
    def __init__(self):
        self._exit_callbacks = []
    
    async def enter_async_context(self, cm):
        """Enters an arbitrary async context manager."""
        result = await cm.__aenter__()
        self.push_async_exit(cm)
        return result
    
    def push_async_exit(self, exit, is_sync=True):
        """Registers an arbitrary callback with the standard __exit__ method."""
        def _exit_wrapper(exc_type, exc_val, exc_tb):
            return exit(exc_type, exc_val, exc_tb)
        self._exit_callbacks.append(_exit_wrapper)
        return _exit_wrapper
    
    def push_async_callback(self, func, *args, **kwds):
        """Registers an arbitrary callback with the standard __exit__ method."""
        async def _exit_wrapper(exc_type, exc_val, exc_tb):
            await func(*args, **kwds)
        self._exit_callbacks.append(_exit_wrapper)
        return func
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *exc_details):
        received_exc = exc_details[0] is not None
        exc = exc_details
        suppressed_exc = False
        
        while self._exit_callbacks:
            exit_func = self._exit_callbacks.pop()
            try:
                result = exit_func(*exc)
                if hasattr(result, '__await__'):
                    result = await result
                if result:
                    suppressed_exc = True
                    exc = (None, None, None)
            except:
                exc = sys.exc_info()
        
        return received_exc and suppressed_exc
    
    async def aclose(self):
        """Immediately unregister all existing context managers."""
        await self.__aexit__(None, None, None)


class suppress:
    """Context manager to suppress specified exceptions."""
    
    def __init__(self, *exceptions):
        self.exceptions = exceptions
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False
        return issubclass(exc_type, self.exceptions)


class redirect_stdout:
    """Context manager for temporarily redirecting stdout."""
    
    def __init__(self, new_target):
        self._new_target = new_target
        self._old_targets = []
    
    def __enter__(self):
        import sys
        self._old_targets.append(sys.stdout)
        sys.stdout = self._new_target
        return self._new_target
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import sys
        sys.stdout = self._old_targets.pop()
        return False


class redirect_stderr:
    """Context manager for temporarily redirecting stderr."""
    
    def __init__(self, new_target):
        self._new_target = new_target
        self._old_targets = []
    
    def __enter__(self):
        import sys
        self._old_targets.append(sys.stderr)
        sys.stderr = self._new_target
        return self._new_target
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import sys
        sys.stderr = self._old_targets.pop()
        return False


class closing:
    """Context manager that calls close() on the thing upon exit."""
    
    def __init__(self, thing):
        self.thing = thing
    
    def __enter__(self):
        return self.thing
    
    def __exit__(self, *exc_info):
        self.thing.close()


class nullcontext:
    """Context manager that does nothing."""
    
    def __init__(self, enter_result=None):
        self.enter_result = enter_result
    
    def __enter__(self):
        return self.enter_result
    
    def __exit__(self, *exc_info):
        return False


class asynccontextmanager:
    """Async context manager from an async generator."""
    
    def __init__(self, func, args, kwds):
        self.func = func
        self.args = args
        self.kwds = kwds
    
    async def __aenter__(self):
        self.gen = self.func(*self.args, **self.kwds)
        return await self.gen.__anext__()
    
    async def __aexit__(self, typ, value, traceback):
        if typ is None:
            try:
                await self.gen.__anext__()
            except StopAsyncIteration:
                return False
            else:
                raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                value = typ()
            try:
                await self.gen.athrow(typ, value, traceback)
            except StopAsyncIteration:
                return True
            except RuntimeError as exc:
                if exc.__cause__ is value:
                    return False
                raise


def contextmanager(func):
    """Decorator for context managers."""
    import functools
    
    @functools.wraps(func)
    def helper(*args, **kwds):
        return _GeneratorContextManager(func, args, kwds)
    return helper


class _GeneratorContextManager:
    """Helper for contextmanager decorator."""
    
    def __init__(self, func, args, kwds):
        self.gen = func(*args, **kwds)
    
    def __enter__(self):
        try:
            return next(self.gen)
        except StopIteration:
            raise RuntimeError("generator didn't yield")
    
    def __exit__(self, typ, value, traceback):
        if typ is None:
            try:
                next(self.gen)
            except StopIteration:
                return False
            else:
                raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                value = typ()
            try:
                self.gen.throw(typ, value, traceback)
            except StopIteration as exc:
                return exc is not value
            except RuntimeError as exc:
                if exc.__cause__ is value:
                    return False
                raise
            except:
                if sys.exc_info()[1] is not value:
                    raise
            return False


def asynccontextmanager(func):
    """Decorator for async context managers."""
    import functools
    
    @functools.wraps(func)
    def helper(*args, **kwds):
        return AsyncContextManager(func, args, kwds)
    return helper


class AsyncContextManager:
    """Helper for asynccontextmanager decorator."""
    
    def __init__(self, func, args, kwds):
        self.func = func
        self.args = args
        self.kwds = kwds
    
    async def __aenter__(self):
        self.gen = self.func(*self.args, **self.kwds)
        try:
            return await self.gen.__anext__()
        except StopAsyncIteration:
            raise RuntimeError("async generator didn't yield")
    
    async def __aexit__(self, typ, value, traceback):
        if typ is None:
            try:
                await self.gen.__anext__()
            except StopAsyncIteration:
                return False
            else:
                raise RuntimeError("async generator didn't stop")
        else:
            if value is None:
                value = typ()
            try:
                await self.gen.athrow(typ, value, traceback)
            except StopAsyncIteration:
                return True
            except RuntimeError as exc:
                if exc.__cause__ is value:
                    return False
                raise
            except:
                if sys.exc_info()[1] is value:
                    raise
            return False
