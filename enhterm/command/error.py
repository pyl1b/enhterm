# -*- coding: utf-8 -*-
"""
Contains the definition of the ErrorCommand class.
"""
import logging

from enhterm.command import Command
from enhterm.command.noop import NoOpCommand

logger = logging.getLogger('et.error')


class ErrorCommand(Command):
    """
    This class indicates that an error condition appeared.

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
        return f'ErrorCommand({self.message})'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return f'ErrorCommand(term={self.term}, ' \
            f'provider={self.provider}, ' \
            f'result={self.result}, ' \
            f'uuid={self.uuid}, ' \
            f'message={self.message})'

    def encode(self):
        """
        Called when a class instance needs to be serialized.

        .. note:
           The `result` and `uuid` members should not be serialized
           in case of :class:`~Command`.
        """
        return self.message

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
        assert isinstance(raw_data, str)
        self.message = raw_data

    @classmethod
    def class_id(cls):
        """
        A unique identifier of the class.

        This value is used as a key when a constructor needs to
        be associated with a string
        (see :class:`enhterm.ser_deser.dsds.DictSerDeSer`).
        """
        return 'error'

    def execute(self):
        """
        Called by the command loop to do some work.

        The return value will be deposited by the command loop it into
        the `result` member.
        """
        self.term.error(self.message)
        return None
