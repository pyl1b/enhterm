# -*- coding: utf-8 -*-
"""
Contains the definition of the NoOpCommand class.
"""
import logging

from enhterm.command import Command

logger = logging.getLogger('et.quit')


class QuitCommand(Command):
    """
    Returning this command will cause the terminal
    to exit the command loop.

    Attributes:
        reason (str):
            The reason the program quits. Simply passed along.
    """

    def __init__(self, reason=None, *args, **kwargs):
        """
        Constructor.

        Arguments:
            reason (str):
                The reason the program quits. Simply passed along.
        """
        super().__init__(*args, **kwargs)
        self.reason = reason

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'QuitCommand()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'QuitCommand()'

    def execute(self):
        """
        Signals the terminal to exit main loop.
        """
        self.term.should_stop = True
        return None

    def encode(self):
        """
        Called when a class instance needs to be serialized.

        .. note:
           The `result` and `uuid` members should not be serialized
           in case of :class:`~Command`.
        """
        return self.reason

    def decode(self, raw_data):
        """
        Apply raw data to this instance.

        It is asserted that correct class has already been constructed
        and that it has `result` and `uuid` members set in case of
        :class:`~Command`..

        Raises:
            DecodeError:
                The implementation should raise this class or a
                subclass of it.

        Arguments:
            raw_data (bytes):
                The data to apply.
        """
        self.reason = raw_data

    @classmethod
    def class_id(cls):
        """
        A unique identifier of the class.

        This value is used as a key when a constructor needs to
        be associated with a string
        (see :class:`enhterm.ser_deser.dsds.DictSerDeSer`).
        """
        return 'quit'
