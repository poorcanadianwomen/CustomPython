"""math module for CustomPython OS.

Mathematical functions (uses built-in mathmodule).
"""

from math import (
    pi,
    e,
    tau,
    inf,
    nan,
    fabs,
    fmod,
    fsum,
    factorial,
    floor,
    ceil,
    trunc,
    exp,
    expm1,
    log,
    log1p,
    log2,
    log10,
    pow,
    sqrt,
    isqrt,
    gcd,
    lcm,
    hypot,
    fabs,
    copysign,
    frexp,
    ldexp,
    modf,
    remainder,
    fma,
    isnan,
    isinf,
    isfinite,
    isnormal,
    signbit,
    nextafter,
    ulp,
    degrees,
    radians,
    cos,
    sin,
    tan,
    acos,
    asin,
    atan,
    atan2,
    cosh,
    sinh,
    tanh,
    acosh,
    asinh,
    atanh,
    erf,
    erfc,
    gamma,
    lgamma,
    dist,
    perm,
    comb,
)


def isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0):
    """Determine whether two floating point numbers are close in value."""
    if rel_tol < 0.0 or abs_tol < 0.0:
        raise ValueError('tolerances must be non-negative')
    
    if a == b:
        return True
    
    if abs(a) == inf or abs(b) == inf:
        return a == b
    
    diff = abs(b - a)
    return diff <= rel_tol * max(abs(a), abs(b)) or diff <= abs_tol


# Additional convenience functions
def gcd(*integers):
    """Return the greatest common divisor of the specified integer arguments."""
    from functools import reduce
    import math
    
    if not integers:
        return 0
    
    def _gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    return reduce(_gcd, integers)


def lcm(*integers):
    """Return the least common multiple of the specified integer arguments."""
    from functools import reduce
    import math
    
    if not integers:
        return 1
    
    def _lcm(a, b):
        return abs(a * b) // math.gcd(a, b)
    
    return reduce(_lcm, integers)


def expm1(x):
    """Return e raised to the power x, minus 1."""
    return math.exp(x) - 1


def log1p(x):
    """Return natural logarithm of 1+x."""
    return math.log(1 + x)


def fsum(iterable):
    """Return an accurate floating point sum of values in the iterable."""
    partials = []
    for x in iterable:
        i = 0
        for p in partials:
            if abs(x) < abs(p):
                x, p = p, x
        hi = x + p
        lo = p - (hi - x)
        if lo:
            partials[i] = lo
            i += 1
        partials[i:] = [hi]
    return sum(partials) if partials else 0.0


def isqrt(n):
    """Return the integer square root of the nonnegative integer n."""
    if n < 0:
        raise ValueError('isqrt() argument must be nonnegative')
    if n == 0:
        return 0
    
    # Newton's method
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def dist(p, q):
    """Return the Euclidean distance between two points."""
    import math
    
    def _sum_of_squares(iterable):
        return sum(x * x for x in iterable)
    
    return math.sqrt(_sum_of_squares(a - b for a, b in zip(p, q)))


def perm(n, k=None):
    """Return the number of ways to choose k items from n items without repetition and with order."""
    import math
    
    if k is None:
        return math.factorial(n)
    if k < 0 or k > n:
        return 0
    return math.factorial(n) // math.factorial(n - k)


def comb(n, k):
    """Return the number of ways to choose k items from n items without repetition and without order."""
    import math
    
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


# Constants
__all__ = [
    'pi', 'e', 'tau', 'inf', 'nan',
    'fabs', 'fmod', 'fsum', 'factorial',
    'floor', 'ceil', 'trunc',
    'exp', 'expm1', 'log', 'log1p', 'log2', 'log10',
    'pow', 'sqrt', 'isqrt', 'gcd', 'lcm', 'hypot',
    'fabs', 'copysign', 'frexp', 'ldexp', 'modf', 'remainder', 'fma',
    'isnan', 'isinf', 'isfinite', 'isnormal', 'signbit', 'nextafter', 'ulp',
    'degrees', 'radians',
    'cos', 'sin', 'tan', 'acos', 'asin', 'atan', 'atan2',
    'cosh', 'sinh', 'tanh', 'acosh', 'asinh', 'atanh',
    'erf', 'erfc', 'gamma', 'lgamma',
    'isclose', 'dist', 'perm', 'comb',
]
