"""re module for CustomPython OS.

Regular expression operations (uses built-in _sre).
"""

from _sre import (
    compile,
    error,
    ASCII,
    IGNORECASE,
    MULTILINE,
    DOTALL,
    VERBOSE,
    A,
    I,
    M,
    S,
    X,
    template,
    escape,
    purge,
    Scanner,
)


def match(pattern, string, flags=0):
    """Try to apply the pattern at the start of the string."""
    return compile(pattern, flags).match(string)


def fullmatch(pattern, string, flags=0):
    """Try to apply the pattern to all of the string."""
    return compile(pattern, flags).fullmatch(string)


def search(pattern, string, flags=0):
    """Scan through string looking for the first location where the pattern produces a match."""
    return compile(pattern, flags).search(string)


def sub(pattern, repl, string, count=0, flags=0):
    """Return the string obtained by replacing the leftmost non-overlapping occurrences."""
    return compile(pattern, flags).sub(repl, string, count)


def subn(pattern, repl, string, count=0, flags=0):
    """Perform a sub() operation and return a 2-tuple (new_string, number_of_subs_made)."""
    return compile(pattern, flags).subn(repl, string, count)


def split(pattern, string, maxsplit=0, flags=0):
    """Split the source string by the occurrences of the pattern."""
    return compile(pattern, flags).split(string, maxsplit)


def findall(pattern, string, flags=0):
    """Return a list of all non-overlapping matches in the string."""
    return compile(pattern, flags).findall(string)


def finditer(pattern, string, flags=0):
    """Return an iterator yielding match objects over all non-overlapping matches."""
    return compile(pattern, flags).finditer(string)


def compile(pattern, flags=0):
    """Compile a regular expression pattern into a regular expression object."""
    import _sre
    return _sre.compile(pattern, flags)


class Match:
    """Match object."""
    
    def __init__(self, string, pos, endpos):
        self.string = string
        self.pos = pos
        self.endpos = endpos
        self.re = None
        self._match = None
    
    def group(self, *args):
        if len(args) == 0:
            return self._match.group() if self._match else None
        elif len(args) == 1:
            return self._match.group(args[0]) if self._match else None
        else:
            return self._match.group(*args) if self._match else None
    
    def groups(self, default=None):
        return self._match.groups(default) if self._match else ()
    
    def groupdict(self, default=None):
        return self._match.groupdict(default) if self._match else {}
    
    def start(self, group=0):
        return self._match.start(group) if self._match else self.pos
    
    def end(self, group=0):
        return self._match.end(group) if self._match else self.pos
    
    def span(self, group=0):
        return self._match.span(group) if self._match else (self.pos, self.pos)
    
    def expand(self, template):
        return self._match.expand(template) if self._match else ''
    
    def __getitem__(self, g):
        return self.group(g)
    
    def __repr__(self):
        return f'<re.Match object; span={self.span()}, match={self.group()!r}>'


class Pattern:
    """Compiled regular expression."""
    
    def __init__(self, pattern, flags=0):
        self.pattern = pattern
        self.flags = flags
    
    def match(self, string, pos=0, endpos=-1):
        return _sre.compile(self.pattern, self.flags).match(string, pos, endpos)
    
    def fullmatch(self, string, pos=0, endpos=-1):
        return _sre.compile(self.pattern, self.flags).fullmatch(string, pos, endpos)
    
    def search(self, string, pos=0, endpos=-1):
        return _sre.compile(self.pattern, self.flags).search(string, pos, endpos)
    
    def sub(self, repl, string, count=0):
        return _sre.compile(self.pattern, self.flags).sub(repl, string, count)
    
    def subn(self, repl, string, count=0):
        return _sre.compile(self.pattern, self.flags).subn(repl, string, count)
    
    def split(self, string, maxsplit=0):
        return _sre.compile(self.pattern, self.flags).split(string, maxsplit)
    
    def findall(self, string, pos=0, endpos=-1):
        return _sre.compile(self.pattern, self.flags).findall(string, pos, endpos)
    
    def finditer(self, string, pos=0, endpos=-1):
        return _sre.compile(self.pattern, self.flags).finditer(string, pos, endpos)
    
    def __repr__(self):
        return f're.compile({self.pattern!r})'
    
    def __eq__(self, other):
        if isinstance(other, Pattern):
            return self.pattern == other.pattern and self.flags == other.flags
        return NotImplemented
    
    def __hash__(self):
        return hash((self.pattern, self.flags))


# Convenience
I = IGNORECASE
L = LOCALE
M = MULTILINE
S = DOTALL
X = VERBOSE
A = ASCII
T = TEMPLATE


def purge():
    """Clear the compiled regular expression cache."""
    pass


def escape(pattern):
    """Escape all non-alphanumerics in pattern."""
    result = []
    for char in pattern:
        if not char.isalnum():
            result.append('\\')
        result.append(char)
    return ''.join(result)


class Scanner:
    """Scanner object."""
    
    def __init__(self, lexicon, flags=0):
        self.lexicon = lexicon
        self.flags = flags
        self._patterns = [(pattern, action) for pattern, action in lexicon.items()]
    
    def scan(self, string):
        result = []
        index = 0
        while index < len(string):
            for pattern, action in self._patterns:
                import re
                match = re.match(pattern, string[index:], self.flags)
                if match:
                    value = action(match.group())
                    if value is not None:
                        result.append(value)
                    index += match.end()
                    break
            else:
                index += 1
        return result, string[index:]
