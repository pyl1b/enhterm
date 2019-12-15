# -*- coding: utf-8 -*-
"""
Contains the definition of the TextProvider class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from enhterm.command.noop import NoOpCommand
from enhterm.command.text import TextCommand
from enhterm.mixins.stream import StreamMixin
from enhterm.provider import Provider

logger = logging.getLogger('et.txt')


class TextProvider(StreamMixin, Provider):
    """
    A provider that simply takes the text and creates a text command for it.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        super().__init__(*args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'TextProvider()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'TextProvider()'

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
            return TextCommand(text)
