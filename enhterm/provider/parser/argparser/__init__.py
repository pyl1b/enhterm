# -*- coding: utf-8 -*-
"""
Contains the definition of the ArgParser class.
"""
import logging
from argparse import ArgumentParser, ArgumentError, Namespace
import shlex

from enhterm.command import Command
from enhterm.command.error import ErrorCommand
from enhterm.command.noop import NoOpCommand
from enhterm.command.text import TextCommand
from enhterm.impl.p2p.p2p_provider import RemoteProvider
from enhterm.provider import Provider
from enhterm.provider.parser import Parser
from enhterm.provider.queue_provider import QueueProvider
from enhterm.provider.text_provider import TextProvider

logger = logging.getLogger('et.argparser')


class ArgParseCommand(Command):
    """
    A command returned by our parser.
    """
    def __init__(self, parsed=None, *args, **kwargs):
        """ Constructor. """
        super().__init__(*args, **kwargs)
        self.parsed = parsed
        if parsed is not None:
            self.call_me = parsed.func
            del parsed.__dict__['func']

            if hasattr(parsed, 'command'):
                # Because we set the dest parameter to 'command' a
                # command attribute is set, with the value of the
                # name of the subparser.
                self.command_name = parsed.command
                del parsed.__dict__['command']
            else:
                # When a subparser was not set or was set but without
                # dest argument.
                self.command_name = None
        else:
            self.command_name = None
            self.call_me = None

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'ArgParseCommand()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'ArgParseCommand()'

    def execute(self):
        """
        Called by the command loop to do some work.

        The return value will be deposited by the command loop it into
        the `result` member.
        """
        return self.call_me(command=self, **self.parsed.__dict__)

    def encode(self):
        """
        Called when a class instance needs to be serialized.

        .. note:
           The `result` and `uuid` members should not be serialized
           in case of :class:`~Command`.
        """
        return self.command_name, self.parsed.__dict__

    def decode(self, raw_data):
        """
        Apply raw data to this instance.

        It is asserted that correct class has already been constructed
        and that it has `result` and `uuid` members set in case of
        :class:`~Command`..

        Raises:
            DecodeError:
                The implementation should raise this class or a
                subclass of it.

        Arguments:
            raw_data (bytes):
                The data to apply.
        """
        assert len(raw_data) == 2
        self.command_name, self.parsed = raw_data
        self.parsed = Namespace(**self.parsed)

    @classmethod
    def class_id(cls):
        """
        A unique identifier of the class.

        This value is used as a key when a constructor needs to
        be associated with a string
        (see :class:`enhterm.ser_deser.dsds.DictSerDeSer`).
        """
        return "argparse"


class ParserError(Exception):
    """ Hops the exceptions back to :meth:`~parse`."""
    pass


class NoOpError(Exception):
    """ :meth:`~parse` should return a :class:`~NoOpCommand`."""
    pass


class ArgParser(ArgumentParser, Parser):
    """
    Parser that uses argparse library to interpret the text.

    Note the two functions of this class: an `enhterm` parser
    and :class:`argparse.ArgumentParser`.

    The usual use of this parser is through subparsers that implement commands.

    >>> from enhterm.provider.parser.argparser import ArgParser
    >>> testee = ArgParser()
    >>> subparsers = testee.add_subparsers(
    >>>     title="commands", dest="command", help="commands")
    >>> def do_add(command, arguments):
    >>>     return sum(arguments.integers)
    >>> parser_add = subparsers.add_parser('add')
    >>> parser_add.add_argument(
    >>>     'integers', metavar='int', nargs='+', type=int,
    >>>     help='an integer to be summed')
    >>> parser_add.set_defaults(func=do_add)
    >>> testee.parse('add -h')
    >>> result = testee.parse('add 1 2 3')
    >>> exec_result = result.execute()

    A simpler variant is:
    >>> from enhterm.provider.parser.argparser import ArgParser
    >>> testee = ArgParser()


    Attributes:

    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Arguments:

        """
        provider = kwargs.pop('provider', None)
        super().__init__(*args, **kwargs)
        assert provider is not None, "The provider must be set and kept " \
                                     "the same for the lifetime of the parser"
        self.provider = provider
        self.prog = ''
        self._subparser_action = None
        self.prefix = ''
        self.suffix = ''

    def add_subparsers(self, **kwargs):
        """
        Monkey-patch add_parser method.

        Parsers created by the sub-parser have same class as
        the main parser (in our case the class:`~ArgParser` class).
        Because we want messages printed by the argparse library
        to go through our watchers, we want to set the parser
        so it is available in :meth:`~_print_message`.

        This is because we don't want to ask the user to place
        this argument themselves each time they create the parser.
        """
        result = super().add_subparsers(**kwargs)
        previous_method = result.add_parser

        def monkey_patch(*args, **my_kw_args):
            return previous_method(*args, **my_kw_args,
                                   provider=self.provider)

        result.add_parser = monkey_patch
        return result

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'ArgParser()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'ArgParser()'

    @property
    def subparsers(self):
        if self._subparser_action is None:
            self._subparser_action = self.add_subparsers(
                title="commands", dest="command", help="commands")
        return self._subparser_action

    def add_parser(self, *args, **kwargs):
        return self.subparsers.add_parser(*args, **kwargs)

    def parse(self, text):
        """
        Convert a text into a command.

        Arguments:
            text (str):
                The text to parse. This should be a full command.
        Returns:
            Command
                The command that resulted from parsing the text.
                If the parsing was unsuccessful the method may return either
                :class:`~NoOpCommand' to keep using the provider or `None` to
                uninstall it.
        """
        try:
            if text.startswith('wrap-commands') or text.startswith('wcs ') or text == 'wcs':
                args = self.parse_args(shlex.split(text))
            else:
                args = self.parse_args(shlex.split(f'{self.prefix}{text}{self.suffix}'))
            return ArgParseCommand(parsed=args)
        except ParserError as exc:
            message = str(exc)
            self.provider.term.error(message)
            return ErrorCommand(message=message)
        except NoOpError:
            return NoOpCommand()

    def error(self, message):
        """
        The parser has encountered an error while interpreting the input.

        This method, according to argparse specs, should not return.
        We raise a custom exception that is caught in :meth:`~parse`
        and we pass along the error message.
        """
        raise ParserError(message)

    def exit(self, status=0, message=None):
        """ Trap any exits left out by other code (help, version). """
        raise NoOpError

    def print_usage(self, file=None):
        self._print_message(self.format_usage(), file)

    def print_help(self, file=None):
        self._print_message(self.format_help(), file)

    def _print_message(self, message, file=None):
        if message:
            assert file is None
            self.provider.term.info(message)


class ArgparseRemoteProvider(RemoteProvider):
    """
    A provider that simply takes the text and creates a text command for it.
    """

    def __init__(self, parser=None, *args, **kwargs):
        """
        Constructor.
        """
        super().__init__(*args, **kwargs)
        if parser:
            self.parser = parser
            parser.provider = self
        else:
            self.parser = ArgParser(provider=self)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'ArgparseRemoteProvider()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'ArgparseRemoteProvider()'

    def enqueue_command(self, command):
        """ Adds a command to the internal list. """
        assert isinstance(command, TextCommand)
        new_command = self.parser.parse(command.content)
        new_command.provider = self
        new_command.uuid = command.uuid
        self.queue.put(new_command)
        return new_command
