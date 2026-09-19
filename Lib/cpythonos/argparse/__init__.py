"""argparse module for CustomPython OS.

Command-line argument parser.
"""

import re
import sys
import os as _os


class _AttributeHolder:
    """Base class for objects with attributes."""
    
    def _get_kwargs(self):
        names = [n for n in dir(self) if not n.startswith('_')]
        return [(n, getattr(self, n)) for n in names]
    
    def _repr_attrs(self):
        namevals = []
        for name, val in self._get_kwargs():
            if val is not self.__class__.__dict__.get(name):
                namevals.append('%s=%r' % (name, val))
        return ', '.join(namevals)
    
    def __repr__(self):
        type_name = type(self).__name__
        return '%s(%s)' % (type_name, self._repr_attrs())


class _ActionsContainer:
    """Container for actions."""
    
    def __init__(self):
        self._actions = []
        self._option_string_actions = {}
        self._action_groups = []
        self._mutually_exclusive_groups = []
        self._defaults = {}
        self._negative_number_matcher = re.compile(r'^-.+?$')
        self._check_value = True
    
    def _get_positional_kwargs(self, dest, **kwargs):
        kwargs = self._get_optional_kwargs(dest, **kwargs)
        del kwargs['option_strings']
        return kwargs
    
    def _get_optional_kwargs(self, dest, option_strings=None, **kwargs):
        if option_strings is None:
            option_strings = []
        
        kwargs['dest'] = dest
        kwargs['option_strings'] = option_strings
        kwargs.setdefault('metavar', None)
        kwargs.setdefault('nargs', None)
        kwargs.setdefault('default', _UNSET)
        kwargs.setdefault('type', None)
        kwargs.setdefault('choices', None)
        kwargs.setdefault('required', False)
        kwargs.setdefault('help', None)
        kwargs.setdefault('metavar', None)
        
        return kwargs
    
    def _populate_actions(self):
        """Populate actions list."""
        pass
    
    def _add_action(self, action):
        self._actions.append(action)
        return action
    
    def _remove_action(self, action):
        self._actions.remove(action)
    
    def _get_optional_actions(self):
        return [action for action in self._actions
                if action.option_strings]
    
    def _get_positional_actions(self):
        return [action for action in self._actions
                if not action.option_strings]
    
    def _get_all_actions(self):
        return self._actions[:]
    
    def _get_mutex_actions(self):
        actions = []
        for group in self._mutually_exclusive_groups:
            actions.extend(group._group_actions)
        return actions


class _ActionsContainer:
    """Container for actions."""
    
    def __init__(self):
        self._actions = []
        self._option_string_actions = {}
        self._action_groups = []
        self._mutually_exclusive_groups = []
        self._defaults = {}
        self._negative_number_matcher = re.compile(r'^-.+?$')
        self._check_value = True
    
    def _get_positional_kwargs(self, dest, **kwargs):
        kwargs = self._get_optional_kwargs(dest, **kwargs)
        del kwargs['option_strings']
        return kwargs
    
    def _get_optional_kwargs(self, dest, option_strings=None, **kwargs):
        if option_strings is None:
            option_strings = []
        
        kwargs['dest'] = dest
        kwargs['option_strings'] = option_strings
        kwargs.setdefault('metavar', None)
        kwargs.setdefault('nargs', None)
        kwargs.setdefault('default', _UNSET)
        kwargs.setdefault('type', None)
        kwargs.setdefault('choices', None)
        kwargs.setdefault('required', False)
        kwargs.setdefault('help', None)
        kwargs.setdefault('metavar', None)
        
        return kwargs
    
    def _populate_actions(self):
        """Populate actions list."""
        pass
    
    def _add_action(self, action):
        self._actions.append(action)
        return action
    
    def _remove_action(self, action):
        self._actions.remove(action)
    
    def _get_optional_actions(self):
        return [action for action in self._actions
                if action.option_strings]
    
    def _get_positional_actions(self):
        return [action for action in self._actions
                if not action.option_strings]
    
    def _get_all_actions(self):
        return self._actions[:]
    
    def _get_mutex_actions(self):
        actions = []
        for group in self._mutually_exclusive_groups:
            actions.extend(group._group_actions)
        return actions


class ArgumentParser(_ActionsContainer):
    """Command-line argument parser."""
    
    def __init__(self, prog=None, usage=None, description=None, epilog=None,
                 parents=None, formatter_class=HelpFormatter,
                 prefix_chars='-', fromfile_prefix_chars=None,
                 argument_default=None, conflict_handler='error',
                 add_help=True, allow_abbrev=True):
        super().__init__()
        
        self.prog = prog or _os.path.basename(sys.argv[0])
        self.usage = usage
        self.description = description
        self.epilog = epilog
        self.formatter_class = formatter_class
        self.prefix_chars = prefix_chars
        self.fromfile_prefix_chars = fromfile_prefix_chars
        self.argument_default = argument_default
        self.conflict_handler = conflict_handler
        self.add_help = add_help
        self.allow_abbrev = allow_abbrev
        
        self._positionals = self.add_argument_group('positional arguments')
        self._optionals = self.add_argument_group('optional arguments')
        self._subparsers = None
        
        if add_help:
            self.add_argument('-h', '--help', action='help', default=_SUPPRESS,
                            help='show this help message and exit')
    
    def add_argument(self, *args, **kwargs):
        """Add an argument."""
        if args and args[0][0] in self.prefix_chars:
            action = self._add_action(self._get_optional_kwargs(*args, **kwargs))
            self._optionals._add_action(action)
        else:
            action = self._add_action(self._get_positional_kwargs(*args, **kwargs))
            self._positionals._add_action(action)
        return action
    
    def add_mutually_exclusive_group(self, required=False):
        """Add a mutually exclusive group."""
        group = MutuallyExclusiveGroup(self, required=required)
        self._mutually_exclusive_groups.append(group)
        return group
    
    def add_argument_group(self, title=None, description=None):
        """Add an argument group."""
        group = ArgumentGroup(self, title, description)
        self._action_groups.append(group)
        return group
    
    def parse_args(self, args=None, namespace=None):
        """Parse arguments."""
        if args is None:
            args = sys.argv[1:]
        else:
            args = list(args)
        
        if namespace is None:
            namespace = Namespace()
        
        for action in self._actions:
            if action.dest is not _SUPPRESS:
                if not hasattr(namespace, action.dest):
                    if action.default is not _SUPPRESS:
                        setattr(namespace, action.dest, action.default)
        
        for i, arg in enumerate(args):
            if arg[0] in self.prefix_chars:
                if len(arg) > 2 and arg[1] in self.prefix_chars:
                    # Long option
                    if '=' in arg:
                        option_string, explicit_value = arg.split('=', 1)
                    else:
                        option_string = arg
                        explicit_value = None
                    
                    action = self._option_string_actions.get(option_string)
                    if action is None:
                        action = self._find_long_option(option_string)
                    
                    if action is None:
                        raise ArgumentError(None, 'unrecognized argument: %s' % arg)
                    
                    if action.nargs == 0:
                        action(self, namespace, None)
                    else:
                        # Get value(s)
                        if explicit_value is not None:
                            values = [explicit_value]
                        else:
                            values = []
                            for j in range(1, action.nargs + 1):
                                if i + j < len(args):
                                    values.append(args[i + j])
                                else:
                                    raise ArgumentError(action, 'expected %s argument(s)' % action.nargs)
                            i += action.nargs - 1
                        
                        action(self, namespace, values)
                else:
                    # Short option(s)
                    for j, c in enumerate(arg[1:], 1):
                        option_string = '-' + c
                        action = self._option_string_actions.get(option_string)
                        if action is None:
                            raise ArgumentError(None, 'unrecognized argument: -%s' % c)
                        
                        if action.nargs == 0:
                            action(self, namespace, None)
                        else:
                            # Get value
                            if j < len(arg) - 1:
                                values = [arg[j+1:]]
                            else:
                                if i + 1 < len(args):
                                    values = [args[i+1]]
                                    i += 1
                                else:
                                    raise ArgumentError(action, 'expected %s argument(s)' % action.nargs)
                            
                            action(self, namespace, values)
                            break
            else:
                # Positional argument
                positional_actions = [a for a in self._positionals._actions
                                     if not hasattr(a, '_seen')]
                if positional_actions:
                    action = positional_actions[0]
                    if action.nargs == 0:
                        action(self, namespace, arg)
                    else:
                        values = [arg]
                        action(self, namespace, values)
        
        # Set defaults
        for action in self._actions:
            if action.dest is not _SUPPRESS:
                if not hasattr(namespace, action.dest):
                    if action.default is not _SUPPRESS:
                        setattr(namespace, action.dest, action.default)
        
        return namespace
    
    def parse_known_args(self, args=None, namespace=None):
        """Parse known arguments, returning unknown arguments."""
        if args is None:
            args = sys.argv[1:]
        else:
            args = list(args)
        
        if namespace is None:
            namespace = Namespace()
        
        unknown = []
        try:
            self.parse_args(args, namespace)
        except SystemExit:
            pass
        
        return namespace, unknown
    
    def _find_long_option(self, option_string):
        """Find long option."""
        for action in self._get_optional_actions():
            for option in action.option_strings:
                if option == option_string:
                    return action
                if self.allow_abbrev and option.startswith(option_string):
                    return action
        return None
    
    def print_help(self, file=None):
        """Print help."""
        if file is None:
            file = sys.stdout
        self.format_help()
        file.write(self.format_help())
    
    def format_help(self):
        """Format help."""
        formatter = self._get_formatter()
        formatter.add_usage(self.usage, self._actions, self._mutually_exclusive_groups)
        formatter.add_text(self.description)
        
        for action_group in self._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._actions)
            formatter.end_section()
        
        formatter.add_text(self.epilog)
        return formatter.format_help()
    
    def _get_formatter(self):
        """Get formatter."""
        return self.formatter_class(
            prog=self.prog,
            max_help_position=24,
            width=None
        )
    
    def exit(self, status=0, message=None):
        """Exit with status and optional message."""
        if message:
            self._print_message(message, sys.stderr)
        sys.exit(status)
    
    def error(self, message):
        """Print error message and exit."""
        self.print_usage(sys.stderr)
        self.exit(2, '%s: error: %s\n' % (self.prog, message))
    
    def print_usage(self, file=None):
        """Print usage."""
        if file is None:
            file = sys.stderr
        self._get_formatter().add_usage(self.usage, self._actions, [])
        file.write(self.format_usage())
    
    def format_usage(self):
        """Format usage."""
        return self._get_formatter().format_usage()


class Namespace(_AttributeHolder):
    """Simple namespace for argument storage."""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __eq__(self, other):
        if not isinstance(other, Namespace):
            return NotImplemented
        return self.__dict__ == other.__dict__
    
    def __contains__(self, key):
        return key in self.__dict__
    
    def __repr__(self):
        args = ', '.join(f'{key}={value!r}' for key, value in sorted(self.__dict__.items()))
        return f'Namespace({args})'
    
    def __getattr__(self, name):
        raise AttributeError(f"'Namespace' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
    
    def __delattr__(self, name):
        if name in self.__dict__:
            del self.__dict__[name]
        else:
            raise AttributeError(f"'Namespace' object has no attribute '{name}'")


class Action(_AttributeHolder):
    """Base class for actions."""
    
    def __init__(self, option_strings, dest, nargs=None, const=None, default=None,
                 type=None, choices=None, required=False, help=None, metavar=None):
        self.option_strings = option_strings
        self.dest = dest
        self.nargs = nargs
        self.const = const
        self.default = default
        self.type = type
        self.choices = choices
        self.required = required
        self.help = help
        self.metavar = metavar
    
    def __call__(self, parser, namespace, values, option_string=None):
        raise NotImplementedError


class _StoreAction(Action):
    """Store action."""
    
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


class _StoreConstAction(Action):
    """Store const action."""
    
    def __init__(self, option_strings, dest, const=None, default=None, **kwargs):
        super().__init__(option_strings, dest, nargs=0, const=const, default=default, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.const)


class _StoreTrueAction(Action):
    """Store true action."""
    
    def __init__(self, option_strings, dest, default=False, **kwargs):
        super().__init__(option_strings, dest, nargs=0, const=True, default=default, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, True)


class _StoreFalseAction(Action):
    """Store false action."""
    
    def __init__(self, option_strings, dest, default=True, **kwargs):
        super().__init__(option_strings, dest, nargs=0, const=False, default=default, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, False)


class _AppendAction(Action):
    """Append action."""
    
    def __call__(self, parser, namespace, values, option_string=None):
        current = getattr(namespace, self.dest, None)
        if current is None:
            current = []
        current.extend(values)
        setattr(namespace, self.dest, current)


class _CountAction(Action):
    """Count action."""
    
    def __init__(self, option_strings, dest, default=0, **kwargs):
        super().__init__(option_strings, dest, nargs=0, default=default, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string=None):
        count = getattr(namespace, self.dest, None)
        if count is None:
            count = 0
        setattr(namespace, self.dest, count + 1)


class _HelpAction(Action):
    """Help action."""
    
    def __init__(self, option_strings, dest=_SUPPRESS, default=_SUPPRESS, **kwargs):
        super().__init__(option_strings, dest, nargs=0, default=default, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        parser.exit()


class _VersionAction(Action):
    """Version action."""
    
    def __init__(self, option_strings, dest=_SUPPRESS, version=None, **kwargs):
        super().__init__(option_strings, dest, nargs=0, **kwargs)
        self.version = version
    
    def __call__(self, parser, namespace, values, option_string=None):
        version = self.version
        if version is None:
            version = '%(prog)s 2.0'
        parser._print_message(version % {'prog': parser.prog}, sys.stdout)
        parser.exit()


class ArgumentError(Exception):
    """Argument error."""
    
    def __init__(self, argument, message):
        self.argument = argument
        self.message = message
    
    def __str__(self):
        if self.argument is not None:
            return '%s: %s' % (self.argument, self.message)
        return self.message


class ArgumentTypeError(Exception):
    """Argument type error."""
    pass


class ArgumentParserError(Exception):
    """Argument parser error."""
    pass


class HelpFormatter:
    """Help formatter."""
    
    def __init__(self, prog, max_help_position=24, width=None):
        self.prog = prog
        self.max_help_position = max_help_position
        self.width = width
        self._current_section = None
        self._help_length = 0
        self._action_max_length = 0
        self._section_level = 0
        self._current_indent = 0
        self._width = width or 70
    
    def start_section(self, heading):
        """Start a section."""
        self._current_section = heading
        if heading:
            self._section_level += 1
            self._indent()
    
    def end_section(self):
        """End a section."""
        if self._current_section:
            self._section_level -= 1
            self._current_section = None
    
    def add_text(self, text):
        """Add text."""
        if text:
            self._write(text)
    
    def add_usage(self, usage, actions, groups, prefix='usage: '):
        """Add usage."""
        if usage is not None:
            usage = usage % dict(prog=self.prog)
        
        prog = '%(prog)s' % dict(prog=self.prog)
        
        if usage is None:
            usage = ' '.join([prog] + 
                           [self._format_usage_action(action) for action in actions
                            if not hasattr(action, '_suppressed')])
        
        self._write(usage)
    
    def _format_usage_action(self, action):
        """Format action for usage."""
        if action.option_strings:
            return action.option_strings[0]
        return action.dest
    
    def add_arguments(self, actions):
        """Add arguments."""
        for action in actions:
            self.add_argument(action)
    
    def add_argument(self, action):
        """Add argument."""
        if action.help is not None:
            self._write(self._format_argument(action))
    
    def format_help(self):
        """Format help."""
        help_text = '\n'.join(self._lines)
        return help_text + '\n'
    
    def _format_argument(self, action):
        """Format argument."""
        if action.option_strings:
            return '  ' + ', '.join(action.option_strings) + '\t' + (action.help or '')
        return '  ' + action.dest + '\t' + (action.help or '')
    
    def _indent(self):
        """Add indent."""
        self._current_indent += 2
    
    def _write(self, text):
        """Write text."""
        if not hasattr(self, '_lines'):
            self._lines = []
        self._lines.append(text)


class ArgumentGroup(_ActionsContainer):
    """Argument group."""
    
    def __init__(self, parser, title=None, description=None):
        super().__init__()
        self._parser = parser
        self._title = title
        self._description = description
        self._group_actions = []
    
    @property
    def title(self):
        return self._title
    
    @property
    def description(self):
        return self._description
    
    def add_argument(self, *args, **kwargs):
        """Add argument."""
        action = super().add_argument(*args, **kwargs)
        self._group_actions.append(action)
        return action


class MutuallyExclusiveGroup(ArgumentGroup):
    """Mutually exclusive group."""
    
    def __init__(self, parser, required=False):
        super().__init__(parser)
        self._required = required
        self._group_actions = []
    
    def add_argument(self, *args, **kwargs):
        """Add argument."""
        action = super().add_argument(*args, **kwargs)
        self._group_actions.append(action)
        return action


_SUPPRESS = '==SUPPRESS=='
_UNSET = object()
