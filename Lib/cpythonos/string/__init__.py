"""string module for CustomPython OS.

Common string operations.
"""

# Constants
ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'
hexdigits = '0123456789abcdefABCDEF'
octdigits = '01234567'
punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
whitespace = ' \t\n\r\x0b\x0c'
printable = ascii_letters + digits + punctuation + whitespace


class Formatter:
    """Base class for string formatting."""
    
    def format(self, format_string, *args, **kwargs):
        """Format the string according to the format string."""
        return format_string.format(*args, **kwargs)
    
    def vformat(self, format_string, args, kwargs):
        """Format the string with explicit mapping of arguments."""
        return format_string.format(*args, **kwargs)
    
    def parse(self, format_string):
        """Parse a format string."""
        result = []
        for literal_text, field_name, format_spec, conversion in \
                self._parse_format_string(format_string):
            result.append((literal_text, field_name, format_spec, conversion))
        return result
    
    def _parse_format_string(self, format_string):
        """Parse a format string into components."""
        result = []
        literal_text = ''
        i = 0
        
        while i < len(format_string):
            if format_string[i] == '{':
                # Start of field
                if literal_text:
                    result.append((literal_text, None, None, None))
                    literal_text = ''
                
                # Find closing brace
                j = i + 1
                depth = 1
                while j < len(format_string) and depth > 0:
                    if format_string[j] == '{':
                        depth += 1
                    elif format_string[j] == '}':
                        depth -= 1
                    j += 1
                
                # Parse field
                field = format_string[i+1:j-1]
                if ':' in field:
                    field_name, format_spec = field.split(':', 1)
                else:
                    field_name = field
                    format_spec = None
                
                if '!' in field_name:
                    field_name, conversion = field_name.split('!', 1)
                else:
                    conversion = None
                
                result.append(('', field_name, format_spec, conversion))
                i = j
            elif format_string[i] == '}':
                # Escaped closing brace
                literal_text += '}'
                i += 2
            else:
                literal_text += format_string[i]
                i += 1
        
        if literal_text:
            result.append((literal_text, None, None, None))
        
        return result
    
    def get_field(self, field_name, args, kwargs):
        """Get a field value from arguments."""
        if field_name is None:
            return None
        
        # Try to convert to integer
        try:
            index = int(field_name)
            return args[index]
        except (ValueError, IndexError):
            pass
        
        # Try to get from kwargs
        return kwargs[field_name]
    
    def get_value(self, key, args, kwargs):
        """Get a value from arguments."""
        if isinstance(key, (int, slice)):
            return args[key]
        return kwargs[key]


# Template string
class Template:
    """String template with $-based substitutions."""
    
    def __init__(self, template):
        self.template = template
    
    def substitute(self, mapping={}, /, **kws):
        """Substitute placeholders with values."""
        import re
        
        def replace(match):
            name = match.group(1)
            if name in mapping:
                return str(mapping[name])
            elif name in kws:
                return str(kws[name])
            elif name.isdigit():
                return ''  # Missing positional
            else:
                raise ValueError(f'Invalid placeholder: ${name}')
        
        return re.sub(r'\$(\w+)', replace, self.template)
    
    def safe_substitute(self, mapping={}, /, **kws):
        """Substitute placeholders, leaving unmatched ones unchanged."""
        import re
        
        def replace(match):
            name = match.group(1)
            if name in mapping:
                return str(mapping[name])
            elif name in kws:
                return str(kws[name])
            else:
                return match.group(0)  # Return unchanged
        
        return re.sub(r'\$(\w+)', replace, self.template)
    
    def is_valid(self):
        """Check if template is valid."""
        import re
        try:
            re.sub(r'\$(\w+)', lambda m: m.group(0), self.template)
            return True
        except:
            return False
    
    def search(self, mapping={}, /, **kws):
        """Search for first placeholder."""
        import re
        match = re.search(r'\$(\w+)', self.template)
        if match:
            name = match.group(1)
            if name in mapping:
                return name, mapping[name]
            elif name in kws:
                return name, kws[name]
        return None
    
    def findall(self, mapping={}, /, **kws):
        """Find all placeholders."""
        import re
        result = []
        for match in re.finditer(r'\$(\w+)', self.template):
            name = match.group(1)
            if name in mapping:
                result.append((name, mapping[name]))
            elif name in kws:
                result.append((name, kws[name]))
        return result
    
    def __repr__(self):
        return f'Template({self.template!r})'


# Formatter and Template classes are already defined above
