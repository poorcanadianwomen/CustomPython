"""configparser module for CustomPython OS.

Configuration file parser.
"""

from configparser import (
    RawConfigParser,
    ConfigParser,
    SectionProxy,
    Interpolation,
    BasicInterpolation,
    ExtendedInterpolation,
    MissingSectionHeaderError,
    ParsingError,
    NoSectionError,
    NoOptionError,
    DuplicateOptionError,
    DuplicateSectionError,
    InterpolationSyntaxError,
    InterpolationDepthError,
    InterpolationMissingOptionError,
)


class ConfigParser(RawConfigParser):
    """Configuration file parser with interpolation."""
    
    SECTCRE = r'\[(?P<header>[^]]+)\]'
    OPTCRE_NV = r'(?P<option>[^:=\s][^:=]*)\s*(?P<vi>[:=])\s*(?P<value>.*)$'
    
    def __init__(self, defaults=None, dict_type=dict, inline_comment_prefixes=None,
                 comment_prefixes=('#', ';'), remove_comments=False,
                 empty_lines_before_values=True):
        super().__init__(defaults=defaults, dict_type=dict_type,
                        inline_comment_prefixes=inline_comment_prefixes,
                        comment_prefixes=comment_prefixes,
                        remove_comments=remove_comments,
                        empty_lines_before_values=empty_lines_before_values)
        self._interpolation = self._DEFAULT_INTERPOLATION()
    
    def optionxform(self, optionstr):
        """Lowercase option names."""
        return optionstr.lower()
    
    def has_option(self, section, option):
        """Check if section and option exist."""
        if section not in self._sections:
            return False
        return option in self._sections[section]
    
    def read(self, filenames, encoding=None):
        """Read configuration files."""
        if isinstance(filenames, str):
            filenames = [filenames]
        
        for filename in filenames:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    self.read_file(f, source=filename)
            except (OSError, IOError):
                continue
    
    def read_file(self, f, source=None):
        """Read configuration from file object."""
        if source is None:
            try:
                source = f.name
            except AttributeError:
                source = '<%s>' % id(f)
        
        self._read(f, source)
    
    def read_string(self, string, source='<string>'):
        """Read configuration from string."""
        from io import StringIO
        self.read_file(StringIO(string), source=source)
    
    def read_dict(self, dictionary, source='<dict>'):
        """Read configuration from dictionary."""
        for section, keys in dictionary.items():
            section = str(section)
            if section not in self._sections:
                self.add_section(section)
            if not isinstance(keys, dict):
                raise TypeError('Keys must be strings')
            for key, value in keys.items():
                key = self.optionxform(str(key))
                if section == self.default_section and key in self._defaults:
                    raise ValueError('option %s already exists in defaults' % key)
                self._sections[section][key] = str(value)
    
    def write(self, fp):
        """Write configuration to file."""
        if self._defaults:
            fp.write('[%s]\n' % self.default_section)
            for key, value in sorted(self._defaults.items()):
                fp.write('%s = %s\n' % (str(key), str(value).replace('\n', '\n\t')))
            fp.write('\n')
        
        for section in sorted(self._sections):
            fp.write('[%s]\n' % section)
            for key, value in sorted(self._sections[section].items()):
                fp.write('%s = %s\n' % (str(key), str(value).replace('\n', '\n\t')))
            fp.write('\n')
    
    def get(self, section, option, *, raw=False, vars=None, fallback=_UNSET):
        """Get option value."""
        d = self._sections.get(section, self._defaults)
        if option not in d:
            if fallback is not _UNSET:
                return fallback
            raise NoSectionError(section)
        
        if raw:
            value = d[option]
        else:
            value = self._interpolation.before_get(self, section, option, d[option], d)
        
        if vars:
            for key, value in vars.items():
                d[key] = str(value)
        
        return value
    
    def items(self, section=_UNSET, raw=False, vars=None):
        """Return items from section."""
        if section is _UNSET:
            d = dict(self._defaults)
        else:
            d = self._sections.get(section, {})
        
        if vars:
            for key, value in vars.items():
                d[key] = str(value)
        
        if raw:
            return list(d.items())
        
        return [(key, self._interpolation.before_get(self, section, key, value, d))
                for key, value in d.items()]
    
    def has_section(self, section):
        """Check if section exists."""
        return section in self._sections
    
    def add_section(self, section):
        """Add a section."""
        if section in self._sections:
            raise DuplicateSectionError(section)
        self._sections[section] = {}
    
    def remove_section(self, section):
        """Remove a section."""
        if section in self._sections:
            del self._sections[section]
            return True
        return False
    
    def remove_option(self, section, option):
        """Remove an option."""
        if section in self._sections:
            if option in self._sections[section]:
                del self._sections[section][option]
                return True
        return False
    
    def set(self, section, option, value=None):
        """Set an option."""
        if section is None:
            section = self.default_section
        
        if section not in self._sections:
            raise NoSectionError(section)
        
        self._sections[section][self.optionxform(option)] = str(value)
    
    def getint(self, section, option, *, raw=False, vars=None, fallback=_UNSET):
        """Get option value as integer."""
        value = self.get(section, option, raw=raw, vars=vars, fallback=fallback)
        if value is _UNSET:
            return fallback
        return int(value)
    
    def getfloat(self, section, option, *, raw=False, vars=None, fallback=_UNSET):
        """Get option value as float."""
        value = self.get(section, option, raw=raw, vars=vars, fallback=fallback)
        if value is _UNSET:
            return fallback
        return float(value)
    
    def getboolean(self, section, option, *, raw=False, vars=None, fallback=_UNSET):
        """Get option value as boolean."""
        value = self.get(section, option, raw=raw, vars=vars, fallback=fallback)
        if value is _UNSET:
            return fallback
        
        if isinstance(value, bool):
            return value
        
        v = value.lower()
        if v in ('1', 'yes', 'true', 'on'):
            return True
        elif v in ('0', 'no', 'false', 'off'):
            return False
        else:
            raise ValueError('Not a boolean: %s' % value)
    
    def getlist(self, section, option, *, raw=False, vars=None, fallback=_UNSET):
        """Get option value as list."""
        value = self.get(section, option, raw=raw, vars=vars, fallback=fallback)
        if value is _UNSET:
            return fallback
        return [item.strip() for item in value.split(',') if item.strip()]


class RawConfigParser:
    """Configuration file parser without interpolation."""
    
    SECTCRE = r'\[(?P<header>[^]]+)\]'
    OPTCRE_NV = r'(?P<option>[^:=\s][^:=]*)\s*(?P<vi>[:=])\s*(?P<value>.*)$'
    
    def __init__(self, defaults=None, dict_type=dict, inline_comment_prefixes=None,
                 comment_prefixes=('#', ';'), remove_comments=False,
                 empty_lines_before_values=True):
        self._sections = {}
        self._defaults = defaults or {}
        self._dict_type = dict_type
        self._inline_comment_prefixes = inline_comment_prefixes or ()
        self._comment_prefixes = comment_prefixes
        self._remove_comments = remove_comments
        self._empty_lines_before_values = empty_lines_before_values
        self.default_section = 'DEFAULT'
    
    def _read(self, fp, fpname):
        """Internal read method."""
        import re
        
        cursect = None
        optname = None
        lineno = 0
        e = None
        
        while True:
            line = fp.readline()
            if not line:
                break
            lineno += 1
            
            # Strip comments
            comment_end = len(line)
            for prefix in self._comment_prefixes:
                if prefix in line:
                    comment_end = min(comment_end, line.index(prefix))
            
            for prefix in self._inline_comment_prefixes:
                if prefix in line:
                    comment_end = min(comment_end, line.index(prefix))
            
            line = line[:comment_end].rstrip()
            
            # Skip empty lines
            if not line:
                if self._empty_lines_before_values and cursect is not None:
                    continue
            
            # Section header
            mo = re.match(self.SECTCRE, line)
            if mo:
                sectname = mo.group('header')
                if sectname == self.default_section:
                    cursect = self._defaults
                elif sectname not in self._sections:
                    cursect = {}
                    self._sections[sectname] = cursect
                else:
                    cursect = self._sections[sectname]
                optname = None
            
            # Option
            elif cursect is not None and line[0] not in self._comment_prefixes:
                mo = re.match(self.OPTCRE_NV, line)
                if mo:
                    optname = mo.group('option')
                    vi = mo.group('vi')
                    if vi in ('=', ':') and ' ' in vi:
                        vi = vi.strip()
                    if vi == '=':
                        oline = line
                        value = mo.group('value').strip()
                        # Handle line continuation
                        while value.endswith('\\'):
                            line = fp.readline()
                            lineno += 1
                            if not line:
                                break
                            value = value[:-1].rstrip() + line.strip()
                    elif vi == ':':
                        value = mo.group('value').strip()
                    else:
                        value = ''
                    
                    cursect[optname] = value
                else:
                    raise MissingSectionHeaderError(fpname, lineno, line)
        
        if cursect is None:
            return
        
        # Check for incomplete state
        if e is not None:
            raise e


_UNSET = object()
