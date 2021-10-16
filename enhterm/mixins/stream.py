# -*- coding: utf-8 -*-
"""
Contains the definition of the StreamProvider class.
"""
import logging
import os
import sys

from enhterm.provider.parser_provider import ParserProvider

logger = logging.getLogger('et.stream')


class StreamMixin(object):
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

    def get_text(self):
        """
        Retrieve next chunk of text.
        """
        if self.prompt_stream is not None:
            try:
                prompt = self.term.replace_in_string(self.term.prompt)
            except KeyError as exc:
                prompt = f'KeyError({exc}) >'

        self.prompt_stream.write(prompt)
        self.prompt_stream.flush()
        result = self.input_stream.readline()

        # End of stream.
        if len(result) == 0:
            return None

        return result.rstrip('\r\n')
