# -*- coding: utf-8 -*-
"""
Contains the definition of the SerDeSer class.
"""
import logging

from enhterm.base import EtBase

logger = logging.getLogger('et.sds')


class SerDeSer(EtBase):
    """
    Serialize and de-serialize commands and messages.

    The class defines the interface that needs to be implemented
    by classes used for converting commands and paragraphs in messages
    into strings of bytes.
    
    The approach for the command is to directly create the bytes
    array. Paragraphs, on the other hand, are just converted to simple types
    and converting them to bytes is outside tje scope of this class.
    The reverse process also works on bytes for commands and on
    basic types for paragraphs.
    
    Attributes:
        term (EnhTerm):
            The terminal where this registry belongs.
    """

    def __init__(self, term=None, *args, **kwargs):
        """
        Constructor.

        Arguments:
            term (EnhTerm):
                The terminal where this registry belongs.
        """
        self.term = term
        super().__init__(*args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'SerDeSer()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'SerDeSer()'

    def pack_command(self, command):
        """
        Prepare the command for being send or stored.

        Arguments:
            command (Command):
                The command to serialize.

        Returns:
            bytes:
                a string of bytes
        """
        raise NotImplementedError

    def unpack_command(self, raw_data):
        """
        Construct a command from raw data.

        Arguments:
            raw_data (bytes):
                The command to de-serialize.

        Returns:
            Command:
                A new command instance constructed from binary data.
        """
        raise NotImplementedError

    def pack_result(self, command, messages):
        """
        Prepare the command result for being send or stored.

        Arguments:
            command (Command):
                The command whose result we're packing here.
            messages (list of Message):
                Messages generated while executing the command.

        Returns:
            bytes:
                a string of bytes
        """
        raise NotImplementedError

    def unpack_result(self, raw_data):
        """
        Construct a result from raw data.

        Arguments:
            raw_data (bytes):
                The result to de-serialize.

        Returns:
            (result, messages):
                The result is a tuple, with first member being the command
                result and the second being messages generated while the
                command was executed.
        """
        raise NotImplementedError

    def encode_paragraph(self, paragraph):
        """
        Used by the :meth:`enhterm.message.Message.encode`.

        Arguments:
            paragraph (Paragraph):
                 The paragraph to encode.
        """
        return paragraph.class_id(), paragraph.encode()

    def decode_paragraph(self, raw_data):
        """
        Used by the :meth:`enhterm.message.Message.decode`.

        Arguments:
            raw_data:
                 The paragraph data.

         Returns:
             Paragraph:
                A constructed paragraph.
        """
        raise NotImplementedError
