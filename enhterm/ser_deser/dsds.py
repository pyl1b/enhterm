# -*- coding: utf-8 -*-
"""
Contains the definition of the SerDeSer class.
"""
import logging
from uuid import UUID

import umsgpack

from enhterm.command.error import ErrorCommand
from enhterm.command.noop import NoOpCommand
from enhterm.command.quit import QuitCommand
from enhterm.command.text import TextCommand
from enhterm.command.unknown import UnknownCommand
from enhterm.errors import CommandDecodeError, DecodeError
from enhterm.message import Message, TextParagraph
from enhterm.ser_deser import SerDeSer

logger = logging.getLogger('et.sds')


class DictSerDeSer(SerDeSer):
    """
    Serialize and de-serialize commands based on a dictionary
    and umsgpack.

    Classes that should be handled by this class must be registered,
    which bassically meand that an id is associated with a constructor
    that takes no arguments. The id is then saved on one side and used
    on the other to recreate the class.
    
    The objects handled by thos class (Command, Paragraph) implement
    the Serializable interface, meaning they have a class_id method
    an encode and a decode method. Once the object
    is constructed the raw bytes or simple types are
    provided to decode method to fully initialize the object.

    Attributes:
        term (EnhTerm):
            The terminal where this registry belongs.
        _registry (dict):
            Maps identifiers to constructor functions or classes.
            This is not to be used directly. Use :meth:`~add_class` and
            :meth:`~rem_class` methods.
    """

    def __init__(self, term=None, *args, **kwargs):
        """
        Constructor.

        Arguments:
            term (EnhTerm):
                The terminal where this registry belongs.
        """
        self.term = term
        self._command_registry = {}
        self._paragraph_registry = {}
        super().__init__(*args, **kwargs)

        self.add_command_class(ErrorCommand)
        self.add_command_class(NoOpCommand)
        self.add_command_class(QuitCommand)
        self.add_command_class(UnknownCommand)
        self.add_command_class(TextCommand)

        self.add_paragraph_class(TextParagraph)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'DictSerDeSer()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'DictSerDeSer()'

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

        return umsgpack.packb((
            command.class_id(),
            command.uuid.bytes,
            command.encode()
        ))

    def unpack_command(self, raw_data):
        """
        Construct a command from raw data.

        Raises:
            DecodeError:
                If the data does not have enough members.
            CommandDecodeError:
                If the uuid of the command is available this exception
                is raised so that we can report back.
            KeyError:
                If class id was not found in internal registry.
        Arguments:
            raw_data (bytes):
                The command to de-serialize.

        Returns:
            Command:
                A new command instance constructed from binary data.
        """
        raw_data = umsgpack.unpackb(raw_data)
        if len(raw_data) != 3:
            raise DecodeError(
                f"Packed data should have 3 members, found {len(raw_data)}")

        class_id, uuid, raw_data = raw_data
        constructor = self._command_registry.get(class_id, None)
        if constructor is None:
            raise CommandDecodeError(
                f"Class id '{class_id}' is not present in internal registry",
                class_id, uuid, raw_data
            )

        result = constructor()
        result.result = None
        result.uuid = UUID(bytes=uuid, version=4)
        result.decode(raw_data)

        return result

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
        return umsgpack.packb((
            command.class_id(), command.uuid.bytes, command.result,
            [message.encode(self) for message in messages]
        ))

    def unpack_result(self, raw_data):
        """
        Construct a result from raw data.

        Raises:
            DecodeError:
                If the data does not have enough members or are
                of wrong type.

        Arguments:
            raw_data (bytes):
                The result to de-serialize.

        Returns:
            class_id
                The id of the command class.
            uuid
                The identification of the command.
            result
                The result of the command.
            messages
                The list of messages that were generated during the
                execution of the command.
        """
        raw_data = umsgpack.unpackb(raw_data)
        if len(raw_data) != 4:
            raise DecodeError(
                f"Packed data should have 4 members, found {len(raw_data)}")

        class_id, uuid, result, raw_messages = raw_data
        # Note: UUID(bytes=uuid, version=4)
        messages = []
        for raw_message in raw_messages:
            message = Message()
            message.decode(raw_message, self)
            messages.append(message)

        return class_id, uuid, result, messages

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
        class_id, raw_data = raw_data
        constructor = self._paragraph_registry.get(class_id, None)
        if constructor is None:
            raise DecodeError(
                f"Class id {class_id} is not present in internal registry",
            )

        paragraph = constructor()
        paragraph.decode(raw_data)
        return paragraph

    def add_command_class(self, constructor, class_id=None):
        """
        Adds a constructor function to internal map.

        Raises:
            KeyError:
                If the id is already present in the registry.

        Arguments:
            constructor:
                Class or constructor function. No arguments are provided
                when this method is called and it is expected to create
                an instance of a class derived from
                :class:`~enhterm.command.Command`.
            class_id (str):
                The key to use. If not provided it is asserted that
                `constructor` is a :class:`~enhterm.command.Command` subclass
                and :meth:`~enhterm.command.Command.class_id` is used to
                retrieve the key.
        """
        if class_id is None:
            class_id = constructor.class_id()

        if class_id in self._command_registry:
            raise KeyError(f'{class_id} is already associated with a '
                           f'constructor ({self._command_registry[class_id]})')
        self._command_registry[class_id] = constructor

    def rem_command_class(self, class_id):
        """
        Remove a key-constructor pair from internal registry.

        Raises:
            KeyError:
                If the id is not present in internal registry.

        Arguments:
            class_id:
                The id to remove.
        """
        return self._command_registry.pop(class_id)

    def has_command_class(self, class_id):
        """
        Tell if an id is present in internal registry.

        Arguments:
            class_id:
                The id to remove.
        """
        return class_id in self._command_registry.pop

    def add_paragraph_class(self, constructor, class_id=None):
        """
        Adds a constructor function to internal map.

        Raises:
            KeyError:
                If the id is already present in the registry.

        Arguments:
            constructor:
                Class or constructor function. No arguments are provided
                when this method is called and it is expected to create
                an instance of a class derived from
                :class:`~enhterm.message.Paragraph`.
            class_id (str):
                The key to use. If not provided it is asserted that
                `constructor` is a :class:`~enhterm.message.Paragraph` subclass
                and :meth:`~enhterm.message.Paragraph.class_id` is used to
                retrieve the key.
        """
        if class_id is None:
            class_id = constructor.class_id()

        if class_id in self._paragraph_registry:
            raise KeyError(f'{class_id} is already associated with a '
                           f'constructor ({self._paragraph_registry[class_id]})')
        self._paragraph_registry[class_id] = constructor

    def rem_paragraph_class(self, class_id):
        """
        Remove a key-constructor pair from internal registry.

        Raises:
            KeyError:
                If the id is not present in internal registry.

        Arguments:
            class_id:
                The id to remove.
        """
        return self._paragraph_registry.pop(class_id)

    def has_paragraph_class(self, class_id):
        """
        Tell if an id is present in internal registry.

        Arguments:
            class_id:
                The id to remove.
        """
        return class_id in self._paragraph_registry.pop
