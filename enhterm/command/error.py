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
