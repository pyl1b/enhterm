# -*- coding: utf-8 -*-
"""
Contains the definition of the NoOpCommand class.
"""
import logging

from enhterm.command.noop import NoOpCommand

logger = logging.getLogger('et.error')


class TextCommand(NoOpCommand):
    """
    This class stores some textul input

    Providers return this command (essentially a
    :class:`~NoOpCommand`) in cases when parsing happens elsewhere.

    When used with :class:`~DictSerDeSer`, the receiver should use
    something like:

    >>> from enhterm.ser_deser.dsds import DictSerDeSer
    >>> encoder = DictSerDeSer()
    >>> encoder.add_command_class(
    >>>     constructor=argparse_from_text, class_id=TextCommand.class_id())

    Attributes:
        content (str):
            The textual representation of the command.
    """

    def __init__(self, content=None, *args, **kwargs):
        """
        Constructor.

        Arguments:
            content (str):
                The textual representation of the command.
        """
        super().__init__(*args, **kwargs)
        self.content = content if content else ''

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return f'TextCommand("{self.content}")'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return f'TextCommand(content="{self.content}")'

    def encode(self):
        """
        Called when a class instance needs to be serialized.

        .. note:
           The `result` and `uuid` members should not be serialized
           in case of :class:`~Command`.
        """
        return self.content

    def decode(self, raw_data):
        """
        Apply raw data to this instance.

        It is asserted that correct class has already been constructed
        and that it has `result` and `uuid` members set in case of
        :class:`~Command`..

        Raises:
            DecodeText:
                The implementation should raise this class or a
                subclass of it.

        Arguments:
            raw_data (bytes):
                The data to apply.
        """
        assert isinstance(raw_data, str)
        self.content = raw_data

    @classmethod
    def class_id(cls):
        """
        A unique identifier of the class.

        This value is used as a key when a constructor needs to
        be associated with a string
        (see :class:`enhterm.ser_deser.dsds.DictSerDeSer`).
        """
        return 'text'
