# -*- coding: utf-8 -*-
"""
Contains the definition of the RemoteWatcher class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from enhterm.watcher import Watcher

logger = logging.getLogger('RemoteWatcher')


class RemoteWatcher(Watcher):
    """
    This class .

    Attributes:

    """

    def __init__(self, provider, *args, **kwargs):
        """
        Constructor.

        Arguments:

        """
        self.provider = provider
        super().__init__(*args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'RemoteWatcher()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'RemoteWatcher()'

    def pre_cmd(self, command):
        """
        The watcher is informed that the terminal is about to execute a command.

        Arguments:
            command (Command):
                The command to be executed.
        """
        pass

    def post_cmd(self, command):
        """
        The watcher is informed that the terminal has executed a command.

        At this point the result is set in the command structure.

        Arguments:
            command (Command):
                The command that was executed.
        """
        pass

    def message_issued(self, message):
        """
        The watcher is informed that the terminal has issued a message.

        Arguments:
            message (Message):
                The message that was issued.
        """
        pass
