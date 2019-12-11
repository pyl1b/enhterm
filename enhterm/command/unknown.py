# -*- coding: utf-8 -*-
"""
Contains the definition of the NoOpCommand class.
"""
import logging

from enhterm.command import Command

logger = logging.getLogger('et.noop')


class UnknownCommand(Command):
    """
    This class .

    Attributes:

    """

    def __init__(self, unknown_content=None, *args, **kwargs):
        """
        Constructor.

        Arguments:

        """
        super().__init__(*args, **kwargs)
        self.unknown_content = unknown_content

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'NoOpCommand()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'NoOpCommand()'

    def execute(self):
        """
        Called by the command loop to do some work.

        The return value will be deposited by the command loop it into
        the `result` member.
        """
        return None
