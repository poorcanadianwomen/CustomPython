"""itertools module for CustomPython OS.

Iterator building blocks.
"""

import sys
from collections.abc import Iterator
from operator import (
    add, mul, eq, ne, lt, gt, le, ge,
    itemgetter, attrgetter, methodcaller,
)


def count(start=0, step=1):
    """Return evenly spaced values starting with number start."""
    n = start
    while True:
        yield n
        n += step


def cycle(iterable):
    """Save contents of iterable and return elements from the copy repeatedly."""
    saved = list(iterable)
    if not saved:
        return
    yield from saved
    while True:
        yield from saved


def repeat(object, times=None):
    """Repeat object endlessly or up to times."""
    if times is None:
        while True:
            yield object
    else:
        for i in range(times):
            yield object


def accumulate(iterable, func=add, *, initial=None):
    """Return running totals."""
    it = iter(iterable)
    total = initial
    if total is None:
        try:
            total = next(it)
        except StopIteration:
            return
    yield total
    for element in it:
        total = func(total, element)
        yield total


def chain(*iterables):
    """Chain iterables together."""
    for iterable in iterables:
        yield from iterable


def chain_from_iterable(iterable):
    """Chain iterables from a single iterable."""
    for iterable in iterable:
        yield from iterable


class chain:
    """Chain iterables together."""
    
    def __init__(self, *iterables):
        self.iterables = iterables
    
    def __iter__(self):
        for iterable in self.iterables:
            yield from iterable
    
    def __next__(self):
        return self.__iter__().__next__()
    
    @classmethod
    def from_iterable(cls, iterable):
        return cls(*iterable)


def compress(data, selectors):
    """Filter elements returning only those that have a corresponding selector."""
    return (d for d, s in zip(data, selectors) if s)


def dropwhile(predicate, iterable):
    """Drop elements while predicate is true, then return the rest."""
    it = iter(iterable)
    for x in it:
        if not predicate(x):
            yield x
            break
    yield from it


def takewhile(predicate, iterable):
    """Return elements while predicate is true."""
    for x in iterable:
        if predicate(x):
            yield x
        else:
            break


def filterfalse(predicate, iterable):
    """Return elements where predicate is false."""
    if predicate is None:
        predicate = bool
    for x in iterable:
        if not predicate(x):
            yield x


def islice(iterable, stop):
    """Return iterator from start to stop."""
    it = iter(iterable)
    for i in range(stop):
        try:
            yield next(it)
        except StopIteration:
            break


def starmap(function, iterable):
    """Apply function to argument lists from iterable."""
    for args in iterable:
        yield function(*args)


def zip_longest(*iterables, fillvalue=None):
    """Zip iterables with fillvalue for missing values."""
    iterators = [iter(it) for it in iterables]
    while iterators:
        result = []
        for it in iterators:
            try:
                result.append(next(it))
            except StopIteration:
                result.append(fillvalue)
        if all(r == fillvalue for r in result):
            break
        yield tuple(result)


def groupby(iterable, key=None):
    """Group consecutive elements with the same key."""
    from itertools import groupby as _groupby
    # Simplified implementation
    result = {}
    for item in iterable:
        k = key(item) if key else item
        if k not in result:
            result[k] = []
        result[k].append(item)
    return result.items()


def tee(iterable, n=2):
    """Return n independent iterators from iterable."""
    iterators = []
    from collections import deque
    deques = [deque() for _ in range(n)]
    
    def _tee(index):
        try:
            while True:
                if deques[index]:
                    yield deques[index].popleft()
                else:
                    value = next(iterable)
                    for d in deques:
                        d.append(value)
        except StopIteration:
            return
    
    return tuple(_tee(i) for i in range(n))


def product(*iterables, repeat=1):
    """Return cartesian product of input iterables."""
    pools = [list(pool) for pool in iterables] * repeat
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def permutations(iterable, r=None):
    """Return successive r-length permutations of elements."""
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n - r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


def combinations(iterable, r):
    """Return successive r-length combinations of elements."""
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        yield tuple(pool[i] for i in indices)


def combinations_with_replacement(iterable, r):
    """Return successive r-length combinations with replacement."""
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[i]
        yield tuple(pool[i] for i in indices)


def zip_longest(*iterables, fillvalue=None):
    """Zip iterables with fillvalue for missing values."""
    iterators = [iter(it) for it in iterables]
    while iterators:
        result = []
        for it in iterators:
            try:
                result.append(next(it))
            except StopIteration:
                result.append(fillvalue)
        if all(r == fillvalue for r in result):
            break
        yield tuple(result)


def batched(iterable, n):
    """Batch data from iterable into tuples of length n."""
    from itertools import islice
    it = iter(iterable)
    while True:
        batch = tuple(islice(it, n))
        if not batch:
            return
        yield batch
