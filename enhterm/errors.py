# -*- coding: utf-8 -*-
"""
"""


class DecodeError(Exception):
    """
    Problem in decoding things.
    """
    pass


class CommandDecodeError(DecodeError):
    """
    Problem in decoding a command.
    """
    def __init__(self, message, command_id=None, uuid=None, raw_data=None):
        """
        Constructor.
        """
        self.command_id = command_id
        self.uuid = uuid
        self.raw_data = raw_data
        super().__init__(message)


class QuitError(Exception):
    """ :meth:`~parse` should return a :class:`~QuitCommand`."""
    pass
