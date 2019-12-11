# -*- coding: utf-8 -*-
"""
Contains the definition of the StreamProvider class.
"""
import logging
import sys

from enhterm.command.noop import NoOpCommand
from enhterm.provider.parser_provider import ParserProvider

logger = logging.getLogger('et.stream')


class StreamProvider(ParserProvider):
    """
    This class .

    Attributes:

    """

    def __init__(self, input_stream=None, prompt_stream=None,
                 *args, **kwargs):
        """
        Constructor.

        Arguments:

        """
        super().__init__(*args, **kwargs)
        self.input_stream = input_stream if input_stream is not None \
            else sys.stdin
        self.prompt_stream = prompt_stream if prompt_stream is not None \
            else sys.stdout

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'StreamProvider()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'StreamProvider()'

    def get_text(self):
        """
        Retrieve next chunk of text.
        """
        self.prompt_stream.write(self.term.prompt)
        result = self.input_stream.readline()

        # End of stream.
        if len(result) == 0:
            return None

        return result.rstrip('\r\n')
