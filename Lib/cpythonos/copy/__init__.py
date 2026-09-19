"""copy module for CustomPython OS.

Shallow and deep copy operations.
"""

import types


def copy(x):
    """Create a shallow copy of x."""
    cls = type(x)
    
    # Handle built-in types efficiently
    if cls is dict:
        return x.copy()
    if cls in (list, tuple, set, frozenset):
        return cls(x)
    
    # Handle class instances
    if hasattr(x, '__copy__'):
        return x.__copy__()
    
    # Handle other types
    if cls is bool or cls is int or cls is float or cls is complex:
        return x
    
    if cls is str:
        return x[:]
    
    if cls is bytes:
        return x[:]
    
    if cls is type(None):
        return x
    
    if hasattr(x, '__class__'):
        # Try to use __reduce_ex__ or __reduce__
        if hasattr(x, '__reduce_ex__'):
            rv = x.__reduce_ex__(4)
        elif hasattr(x, '__reduce__'):
            rv = x.__reduce__()
        else:
            return x
        
        if isinstance(rv, str):
            return x
        
        if isinstance(rv, tuple):
            if len(rv) == 2:
                constructor, args = rv
                return constructor(*args)
            elif len(rv) >= 3:
                state = rv[1]
                if state is not None:
                    if hasattr(x, '__setstate__'):
                        # Create a copy and set state
                        copier = copy
                        y = copier(x)
                        y.__setstate__(state)
                        return y
                return x
    
    return x


def deepcopy(x, memo=None, _nil=[]):
    """Create a deep copy of x."""
    if memo is None:
        memo = {}
    
    # Check for already copied objects
    d = id(x)
    if d in memo:
        return memo[d]
    
    cls = type(x)
    
    # Handle built-in types efficiently
    if cls is dict:
        y = {}
        memo[d] = y
        for key, value in x.items():
            y[deepcopy(key, memo)] = deepcopy(value, memo)
        return y
    
    if cls is list:
        y = []
        memo[d] = y
        for item in x:
            y.append(deepcopy(item, memo))
        return y
    
    if cls is tuple:
        y = []
        memo[d] = y
        for item in x:
            y.append(deepcopy(item, memo))
        y = tuple(y)
        memo[d] = y
        return y
    
    if cls is set:
        y = set()
        memo[d] = y
        for item in x:
            y.add(deepcopy(item, memo))
        return y
    
    if cls is frozenset:
        y = []
        memo[d] = y
        for item in x:
            y.append(deepcopy(item, memo))
        y = frozenset(y)
        memo[d] = y
        return y
    
    if cls is bool or cls is int or cls is float or cls is complex:
        return x
    
    if cls is str:
        return x[:]
    
    if cls is bytes:
        return x[:]
    
    if cls is type(None):
        return x
    
    # Handle class instances
    if hasattr(x, '__deepcopy__'):
        return x.__deepcopy__(memo)
    
    if hasattr(x, '__copy__'):
        return x.__copy__()
    
    # Handle other types
    if hasattr(x, '__class__'):
        if hasattr(x, '__reduce_ex__'):
            rv = x.__reduce_ex__(4)
        elif hasattr(x, '__reduce__'):
            rv = x.__reduce__()
        else:
            memo[d] = x
            return x
        
        if isinstance(rv, str):
            memo[d] = x
            return x
        
        if isinstance(rv, tuple):
            if len(rv) == 2:
                constructor, args = rv
                args = deepcopy(args, memo)
                y = constructor(*args)
                memo[d] = y
                return y
            elif len(rv) >= 3:
                state = rv[1]
                if state is not None:
                    if hasattr(x, '__setstate__'):
                        y = deepcopy(x, memo)
                        y.__setstate__(deepcopy(state, memo))
                        memo[d] = y
                        return y
                memo[d] = x
                return x
    
    memo[d] = x
    return x


class _EmptyClass:
    """Dummy class for deepcopy."""
    pass


def _reconstruct(x, memo, func, args,
                  state=None, listiter=None, dictiter=None,
                  state_setter=None, obj=None):
    """Reconstruct an object from copy protocol."""
    y = func(*args)
    
    if state is not None:
        if hasattr(y, '__setstate__'):
            y.__setstate__(state)
    
    if listiter is not None:
        for item in listiter:
            y.append(item)
    
    if dictiter is not None:
        for key, value in dictiter:
            y[key] = value
    
    return y


class _EmptyClass:
    """Dummy class for deepcopy."""
    pass


def _reconstruct(x, memo, func, args,
                  state=None, listiter=None, dictiter=None,
                  state_setter=None, obj=None):
    """Reconstruct an object from copy protocol."""
    y = func(*args)
    
    if state is not None:
        if hasattr(y, '__setstate__'):
            y.__setstate__(state)
    
    if listiter is not None:
        for item in listiter:
            y.append(item)
    
    if dictiter is not None:
        for key, value in dictiter:
            y[key] = value
    
    return y


# Replace patterns
_replace = copy
_replace.__doc__ = "Create a shallow copy of x."
