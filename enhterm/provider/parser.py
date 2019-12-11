# -*- coding: utf-8 -*-
"""
Contains the definition of the Parser class.
"""
import logging

from enhterm.base import EtBase

logger = logging.getLogger('et.parser')


class Parser(EtBase):
    """
    Parser for :class:`~ParserProvider`.
    """
    def __init__(self, provider=None, *args, **kwargs):
        """
        Constructor.
        """
        super().__init__(*args, **kwargs)
        self.provider = provider

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'Parser()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'Parser()'

    def parse(self, text):
        """
        Convert a text into a command.

        Arguments:
            text (str):
                The text to parse. This should be a full command.
        """
        raise NotImplementedError
