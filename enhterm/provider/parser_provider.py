# -*- coding: utf-8 -*-
"""
Contains the definition of the ParserProvider class.
"""
import logging

from enhterm.command.noop import NoOpCommand
from enhterm.provider import Provider

logger = logging.getLogger('et.pp')


class ParserProvider(Provider):
    """
    A provider that uses a parser to interpret textual input.

    The instance stores a parser that interprets a chunk of text.
    The implementation must retrieve the full content of the command
    via :meth:`~get_text`

    Attributes:
        parser:
            the parser that will interpret the text.
    """

    def __init__(self, parser=None, *args, **kwargs):
        """
        Constructor.

        Arguments:
            parser:
                the parser that will interpret the text.
        """
        super().__init__(*args, **kwargs)
        self.parser = parser
        if parser is not None:
            parser.provider = self

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'ParserProvider()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'ParserProvider()'

    def get_command(self):
        """
        Retrieve next command to execute.

        This method is only called when the provider is the active one.

        Returns:
            Command or None
                The function must return either a command instance or None,
                in which case the provider will be uninstalled.
        """
        text = self.get_text()
        if text is None:
            return None
        elif len(text) == 0:
            return NoOpCommand(provider=self)
        else:
            return self.parser.parse(text)

    def get_text(self):
        """
        Retrieve next chunk of text.
        """
        raise NotImplementedError
