# -*- coding: utf-8 -*-
"""
Contains the definition of the StreamProvider class.
"""
import logging
import sys

from enhterm.mixins.stream import StreamMixin
from enhterm.provider.parser_provider import ParserProvider

logger = logging.getLogger('et.stream')


class StreamProvider(StreamMixin, ParserProvider):
    """
    A class that takes input from a stream and parses the resulted text.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        super().__init__(*args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'StreamProvider()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'StreamProvider()'
