# -*- coding: utf-8 -*-
"""
Contains the definition of the NoOpCommand class.
"""
import logging

from enhterm.command import Command

logger = logging.getLogger('et.noop')


class NoOpCommand(Command):
    """
    A command that does nothing.

    When providers return `None` they get uninstalled from the terminal.
    This is an alternative that keeps them alive.
    """

    def __init__(self, *args, **kwargs):
        """ Constructor. """
        super().__init__(*args, **kwargs)

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

    def encode(self):
        """
        Called when a class instance needs to be serialized.

        .. note:
           The `result` and `uuid` members should not be serialized
           in case of :class:`~Command`.
        """
        return None

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
        assert raw_data is None

    @classmethod
    def class_id(cls):
        """
        A unique identifier of the class.

        This value is used as a key when a constructor needs to
        be associated with a string
        (see :class:`enhterm.ser_deser.dsds.DictSerDeSer`).
        """
        return 'noop'
