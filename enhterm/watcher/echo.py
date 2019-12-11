# -*- coding: utf-8 -*-
"""
Contains the definition of the EchoWatcher class.
"""
import logging
import sys

from enhterm.watcher import Watcher

logger = logging.getLogger('EchoWatcher')


class EchoWatcher(Watcher):
    """
    A watcher that prints messages to text streams.

    If no streams are provided the watcher will print to stdout and stderr.

    Attributes:
        low_stream (TextIOBase):
            The stream used for messages with severity below `cutoff`.
        high_stream (TextIOBase):
            The stream used for messages with severity equal or above `cutoff`.
        cutoff (int):
            Messages have a `severity` member that is an integer from 0 to
            infinity(but usually to 50). The watcher compares `cutoff` with
            `severity` and decides on which chanel it should send the output.
    """

    def __init__(self, low_stream=None, high_stream=None,
                 cutoff=logging.WARNING, *args, **kwargs):
        """
        Constructor.

        Arguments:
            low_stream (TextIOBase):
                The stream used for messages with severity below `cutoff`.
                Defaults to `stdout`.
            high_stream (TextIOBase):
                The stream used for messages with severity equal or above `cutoff`.
                Defaults to `stderr`.
            cutoff (int):
                Messages have a `severity` member that is an integer from 0 to
                infinity(but usually to 50). The watcher compares `cutoff` with
                `severity` and decides on which chanel it should send the output.
                Defaults to `WARNING`.
        """
        super().__init__(*args, **kwargs)
        self.low_stream = low_stream if low_stream else sys.stdout
        self.high_stream = high_stream if high_stream else sys.stderr
        self.cutoff = cutoff

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'EchoWatcher()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'EchoWatcher()'

    def message_issued(self, message):
        """
        The watcher is informed that the terminal has issued a message.

        Arguments:
            message (Message):
                The message that was issued.
        """
        out = self.low_stream if message.severity < self.cutoff \
            else self.high_stream
        for par in message.paragraphs:
            out.write(str(par))
