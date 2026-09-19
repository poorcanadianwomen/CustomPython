"""textwrap module for CustomPython OS.

Text wrapping and filling.
"""

import re


def wrap(text, width=70, **kwargs):
    """Wrap a single paragraph of text."""
    return TextWrapper(width=width, **kwargs).wrap(text)


def fill(text, width=70, **kwargs):
    """Fill a single paragraph of text."""
    return TextWrapper(width=width, **kwargs).fill(text)


def shorten(text, width, placeholder='...', *, fix_sentence_endings=False,
            break_long_words=True, break_on_hyphens=True):
    """Wrap a single paragraph of text, shortening if necessary."""
    wrapper = TextWrapper(width=width, break_long_words=break_long_words,
                         break_on_hyphens=break_on_hyphens)
    text = wrapper.fill(text)
    
    if len(text) <= width:
        return text
    
    # Shorten
    text = text[:width - len(placeholder)]
    
    # Try to break at word boundary
    last_space = text.rfind(' ')
    if last_space != -1:
        text = text[:last_space]
    
    return text + placeholder


def dedent(text):
    """Remove any common leading whitespace from all lines in text."""
    lines = text.split('\n')
    
    # Find common leading whitespace
    margin = None
    for line in lines:
        stripped = line.lstrip()
        if stripped:
            current_margin = line[:len(line) - len(stripped)]
            if margin is None:
                margin = current_margin
            else:
                margin = margin[:min(len(margin), len(current_margin))]
                # Check if current margin is prefix of margin
                if not margin.startswith(current_margin[:len(margin)]):
                    margin = ''
    
    if margin is None:
        return text
    
    # Remove common leading whitespace
    result = []
    for line in lines:
        if line:
            result.append(line[len(margin):])
        else:
            result.append('')
    
    return '\n'.join(result)


def indent(text, prefix='    ', predicate=None):
    """Add a prefix to all lines of text."""
    if predicate is None:
        def predicate(line):
            return line.strip()
    
    lines = text.split('\n')
    result = []
    for line in lines:
        if predicate(line):
            result.append(prefix + line)
        else:
            result.append(line)
    
    return '\n'.join(result)


def hangindent(text, width, initial_indent='    ', subsequent_indent='    '):
    """Wrap text with hanging indent."""
    wrapper = TextWrapper(width=width, initial_indent=initial_indent,
                         subsequent_indent=subsequent_indent)
    return wrapper.fill(text)


def fillparagraphs(text, width):
    """Fill multiple paragraphs."""
    paragraphs = text.split('\n\n')
    result = []
    for paragraph in paragraphs:
        result.append(fill(paragraph, width))
    return '\n\n'.join(result)


class TextWrapper:
    """Text wrapping class."""
    
    def __init__(self, width=70, initial_indent='', subsequent_indent='',
                 expand_tabs=True, replace_whitespace=True,
                 break_long_words=True, drop_whitespace=True,
                 break_on_hyphens=True, break_on_hyphens=True,
                 break_long_lines=True):
        self.width = width
        self.initial_indent = initial_indent
        self.subsequent_indent = subsequent_indent
        self.expand_tabs = expand_tabs
        self.replace_whitespace = replace_whitespace
        self.break_long_words = break_long_words
        self.drop_whitespace = drop_whitespace
        self.break_on_hyphens = break_on_hyphens
        self.break_long_lines = break_long_lines
        
        # Initialize word delimiter regex
        self._wordsep = re.compile(
            r'( [ \t]* | '              # any whitespace
            r'(?<=[\t\x20]) |           # or a tab/space followed by something
            r'(?<=[^\x20\t]) (?=[^\x20\t]) |  # or two non-whitespace separated by space
            r'(?<=[^\x20\t]) (?=[^\x20\t]) )'  # or two non-whitespace separated by space
        )
        
        self._wordsep_re = re.compile(
            r'( [ \t]* |              '
            r'(?<=[\t\x20]) |         '
            r'(?<=[^\x20\t]) (?=[^\x20\t]) |  '
            r'(?<=[^\x20\t]) (?=[^\x20\t]) )'
        )
    
    def wrap(self, text):
        """Wrap a single paragraph of text."""
        return self._wrap_chunks(self._split_chunks(text))
    
    def fill(self, text):
        """Fill a single paragraph of text."""
        return '\n'.join(self.wrap(text))
    
    def _split_chunks(self, text):
        """Split text into chunks (words and whitespace)."""
        if self.expand_tabs:
            text = text.expandtabs()
        if self.replace_whitespace:
            text = text.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')
        
        # Split into words and whitespace
        chunks = []
        for chunk in text.split(' '):
            if chunk:
                chunks.append(chunk)
            else:
                chunks.append('')
        
        return chunks
    
    def _wrap_chunks(self, chunks):
        """Wrap a list of chunks."""
        lines = []
        current_line = []
        current_length = 0
        
        indent = self.initial_indent
        indent_length = len(indent)
        
        for chunk in chunks:
            # Check if adding this chunk would exceed width
            chunk_length = len(chunk)
            
            if current_length + chunk_length + len(current_line) > self.width:
                if current_line:
                    lines.append(indent + ' '.join(current_line))
                    current_line = []
                    current_length = 0
                    indent = self.subsequent_indent
                    indent_length = len(indent)
                
                if chunk_length > self.width and self.break_long_words:
                    # Break long word
                    while chunk:
                        available = self.width - current_length - indent_length
                        if available <= 0:
                            break
                        line = chunk[:available]
                        chunk = chunk[available:]
                        if line:
                            current_line.append(line)
                            lines.append(indent + ' '.join(current_line))
                            current_line = []
                            current_length = 0
                else:
                    current_line.append(chunk)
                    current_length += chunk_length
            else:
                current_line.append(chunk)
                current_length += chunk_length
        
        if current_line:
            lines.append(indent + ' '.join(current_line))
        
        return lines


def shorten(text, width, placeholder='...', *, fix_sentence_endings=False,
            break_long_words=True, break_on_hyphens=True):
    """Wrap a single paragraph of text, shortening if necessary."""
    wrapper = TextWrapper(width=width, break_long_words=break_long_words,
                         break_on_hyphens=break_on_hyphens)
    text = wrapper.fill(text)
    
    if len(text) <= width:
        return text
    
    # Shorten
    text = text[:width - len(placeholder)]
    
    # Try to break at word boundary
    last_space = text.rfind(' ')
    if last_space != -1:
        text = text[:last_space]
    
    return text + placeholder


def capwords(s, sep=None):
    """Capitalize all words in a string."""
    if sep is None:
        return ' '.join(word.capitalize() for word in s.split())
    return sep.join(word.capitalize() for word in s.split(sep))


class TextWrapper:
    """Text wrapping class."""
    
    unicode_whitespace_trans = {}
    unicode_whitespace_trans[ord('\t')] = ' '
    unicode_whitespace_trans[ord('\n')] = ' '
    unicode_whitespace_trans[ord('\r')] = ' '
    unicode_whitespace_trans[ord('\x0c')] = ' '
    
    def __init__(self, width=70, initial_indent='', subsequent_indent='',
                 expand_tabs=True, replace_whitespace=True,
                 break_long_words=True, drop_whitespace=True,
                 break_on_hyphens=True, break_long_lines=True,
                 fix_sentence_endings=False):
        self.width = width
        self.initial_indent = initial_indent
        self.subsequent_indent = subsequent_indent
        self.expand_tabs = expand_tabs
        self.replace_whitespace = replace_whitespace
        self.break_long_words = break_long_words
        self.drop_whitespace = drop_whitespace
        self.break_on_hyphens = break_on_hyphens
        self.break_long_lines = break_long_lines
        self.fix_sentence_endings = fix_sentence_endings
        
        self._wordsep = re.compile(
            r'( [ \t]* |              '
            r'(?<=[\t\x20]) |         '
            r'(?<=[^\x20\t]) (?=[^\x20\t]) |  '
            r'(?<=[^\x20\t]) (?=[^\x20\t]) )'
        )
        
        self._wordsep_re = re.compile(
            r'( [ \t]* |              '
            r'(?<=[\t\x20]) |         '
            r'(?<=[^\x20\t]) (?=[^\x20\t]) |  '
            r'(?<=[^\x20\t]) (?=[^\x20\t]) )'
        )
    
    def wrap(self, text):
        """Wrap a single paragraph of text."""
        return self._wrap_chunks(self._split_chunks(text))
    
    def fill(self, text):
        """Fill a single paragraph of text."""
        return '\n'.join(self.wrap(text))
    
    def _split_chunks(self, text):
        """Split text into chunks (words and whitespace)."""
        if self.expand_tabs:
            text = text.expandtabs()
        if self.replace_whitespace:
            text = text.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')
        
        # Split into words and whitespace
        chunks = []
        for chunk in text.split(' '):
            if chunk:
                chunks.append(chunk)
            else:
                chunks.append('')
        
        return chunks
    
    def _wrap_chunks(self, chunks):
        """Wrap a list of chunks."""
        lines = []
        current_line = []
        current_length = 0
        
        indent = self.initial_indent
        indent_length = len(indent)
        
        for chunk in chunks:
            # Check if adding this chunk would exceed width
            chunk_length = len(chunk)
            
            if current_length + chunk_length + len(current_line) > self.width:
                if current_line:
                    lines.append(indent + ' '.join(current_line))
                    current_line = []
                    current_length = 0
                    indent = self.subsequent_indent
                    indent_length = len(indent)
                
                if chunk_length > self.width and self.break_long_words:
                    # Break long word
                    while chunk:
                        available = self.width - current_length - indent_length
                        if available <= 0:
                            break
                        line = chunk[:available]
                        chunk = chunk[available:]
                        if line:
                            current_line.append(line)
                            lines.append(indent + ' '.join(current_line))
                            current_line = []
                            current_length = 0
                else:
                    current_line.append(chunk)
                    current_length += chunk_length
            else:
                current_line.append(chunk)
                current_length += chunk_length
        
        if current_line:
            lines.append(indent + ' '.join(current_line))
        
        return lines
