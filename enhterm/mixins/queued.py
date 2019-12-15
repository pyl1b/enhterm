# -*- coding: utf-8 -*-
"""
Contains the definition of the QueueMixin class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from queue import Queue, Empty

from enhterm.command.noop import NoOpCommand

logger = logging.getLogger('QueueMixin')


class QueueMixin(object):
    """
    This class .

    Attributes:

    """

    def __init__(self, initial=None, block=True, timeout=None,
                 close_on_empty=True, *args, **kwargs):
        """
        Constructor.

        Arguments:

        """
        super().__init__(*args, **kwargs)
        self.queue = Queue()
        self.block = block
        self.timeout = timeout
        if initial is not None:
            for item in initial:
                self.queue.put(item)

        self.on_empty = None if close_on_empty else NoOpCommand

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'QueueMixin()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'QueueMixin()'

    def get_command(self):
        """
        Retrieve next command to execute.

        This method is only called when the provider is the active one.

        Returns:
            Command or None
                The function must return either a command instance or None,
                in which case the provider will be uninstalled.
        """
        try:
            cmd = self.queue.get(block=self.block, timeout=self.timeout)
            cmd.provider = self
            return cmd
        except Empty:
            if self.on_empty is None:
                return None
            else:
                return self.on_empty(provider=self)

    def enqueue_command(self, command):
        """ Adds a command to the internal list. """
        command.provider = self
        self.queue.put(command)
        return command
