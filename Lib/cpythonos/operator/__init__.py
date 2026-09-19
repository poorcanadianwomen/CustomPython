"""operator module for CustomPython OS.

Standard operator as functions.
"""


def add(a, b):
    """Return a + b."""
    return a + b


def sub(a, b):
    """Return a - b."""
    return a - b


def mul(a, b):
    """Return a * b."""
    return a * b


def truediv(a, b):
    """Return a / b."""
    return a / b


def floordiv(a, b):
    """Return a // b."""
    return a // b


def mod(a, b):
    """Return a % b."""
    return a % b


def pow(a, b):
    """Return a ** b."""
    return a ** b


def matmul(a, b):
    """Return a @ b."""
    return a @ b


def neg(a):
    """Return -a."""
    return -a


def pos(a):
    """Return +a."""
    return +a


def abs(a):
    """Return abs(a)."""
    return abs(a)


def inv(a):
    """Return ~a."""
    return ~a


def and_(a, b):
    """Return a & b."""
    return a & b


def or_(a, b):
    """Return a | b."""
    return a | b


def xor(a, b):
    """Return a ^ b."""
    return a ^ b


def lshift(a, b):
    """Return a << b."""
    return a << b


def rshift(a, b):
    """Return a >> b."""
    return a >> b


def eq(a, b):
    """Return a == b."""
    return a == b


def ne(a, b):
    """Return a != b."""
    return a != b


def lt(a, b):
    """Return a < b."""
    return a < b


def le(a, b):
    """Return a <= b."""
    return a <= b


def gt(a, b):
    """Return a > b."""
    return a > b


def ge(a, b):
    """Return a >= b."""
    return a >= b


def not_(a):
    """Return not a."""
    return not a


def truth(a):
    """Return True if a is true."""
    return bool(a)


def is_(a, b):
    """Return a is b."""
    return a is b


def is_not(a, b):
    """Return a is not b."""
    return a is not b


def contains(a, b):
    """Return b in a."""
    return b in a


def countOf(a, b):
    """Return the number of occurrences of b in a."""
    return a.count(b)


def indexOf(a, b):
    """Return the index of the first occurrence of b in a."""
    return a.index(b)


def concat(a, b):
    """Return a + b."""
    return a + b


def repeat(a, b):
    """Return a * b."""
    return a * b


def itemgetter(*items):
    """Return a callable that fetches item(s) from its operand."""
    if len(items) == 1:
        item = items[0]
        def func(obj):
            return obj[item]
    else:
        def func(obj):
            return tuple(obj[item] for item in items)
    func.__name__ = 'itemgetter'
    return func


def attrgetter(*attrs):
    """Return a callable that fetches attribute(s) from its operand."""
    if len(attrs) == 1:
        attr = attrs[0]
        def func(obj):
            return getattr(obj, attr)
    else:
        def func(obj):
            return tuple(getattr(obj, attr) for attr in attrs)
    func.__name__ = 'attrgetter'
    return func


def methodcaller(name, /, *args, **kwargs):
    """Return a callable that calls method name on its operand."""
    def func(obj):
        return getattr(obj, name)(*args, **kwargs)
    func.__name__ = 'methodcaller'
    return func


def iadd(a, b):
    """a += b."""
    a += b
    return a


def isub(a, b):
    """a -= b."""
    a -= b
    return a


def imul(a, b):
    """a *= b."""
    a *= b
    return a


def itruediv(a, b):
    """a /= b."""
    a /= b
    return a


def ifloordiv(a, b):
    """a //= b."""
    a //= b
    return a


def imod(a, b):
    """a %= b."""
    a %= b
    return a


def ipow(a, b):
    """a **= b."""
    a **= b
    return a


def iand(a, b):
    """a &= b."""
    a &= b
    return a


def ior(a, b):
    """a |= b."""
    a |= b
    return a


def ixor(a, b):
    """a ^= b."""
    a ^= b
    return a


def ilshift(a, b):
    """a <<= b."""
    a <<= b
    return a


def irshift(a, b):
    """a >>= b."""
    a >>= b
    return a


def iconcat(a, b):
    """a += b."""
    a += b
    return a


def irepeat(a, b):
    """a *= b."""
    a *= b
    return a


def length_hint(obj, default=0):
    """Return an estimate for the length of obj."""
    try:
        return len(obj)
    except TypeError:
        pass
    
    if hasattr(obj, '__length_hint__'):
        try:
            hint = obj.__length_hint__()
            if not isinstance(hint, int):
                raise TypeError('length_hint must be integer')
            if hint < 0:
                raise ValueError('length_hint must be >= 0')
            return hint
        except (TypeError, AttributeError, ValueError):
            pass
    
    return default
