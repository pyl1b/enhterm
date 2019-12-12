# -*- coding: utf-8 -*-
"""
Contains the definition of the NoOpCommand class.
"""
import logging

from enhterm.command.noop import NoOpCommand

logger = logging.getLogger('et.error')


class ErrorCommand(NoOpCommand):
    """
    This class indicates that an error condition appeared..

    Providers return this command (essentially a
    :class:`~NoOpCommand`) to indicate that they have failed to
    retrieve the command.

    Attributes:
        message (str):
            An optional error message describing what went wrong.
    """

    def __init__(self, message=None, *args, **kwargs):
        """
        Constructor.

        Arguments:
            message (str):
                An optional error message describing what went wrong.
        """
        super().__init__(*args, **kwargs)
        self.message = message if message else ''

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'ErrorCommand()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'ErrorCommand()'
