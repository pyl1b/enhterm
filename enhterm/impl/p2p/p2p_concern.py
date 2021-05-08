# -*- coding: utf-8 -*-
"""
Contains the definition of the RemoteConcern class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from p2p0mq.concerns.base import Concern
from p2p0mq.constants import TRACE
from p2p0mq.message import Message

logger = logging.getLogger('RemoteConcern')


class RemoteConcern(Concern):
    """
    Concern that mediates communication between hosts.

    In p2p0mq library the :class:`Concern` is the class that is present on both
    sides of the connection and deals with creation of messages, processing
    the requests, sending back replies and processing those replies. Thus
    the code that deals with a message type is all packed in a single class
    instance.

    On the side which wants to execute a command on
    a remote host we start by :meth:`~compose`-ing the
    message from a command. To keep things generic
    we use an encoder that translates commands into bytes.
    The user has to enqueue the message but we store
    the message to keep track of it.

    The enqueued message is sent to a remote host where
    this concern ia also installed. The :meth:`~process_request`method receives the
    message and decodes the command using same encoder.
    On this side of the connection we keep track of both
    the message and the command. Thr command is placed in the
    providers queue from where it will be picked up and executed.

    Once the command completes it will be sent to :meth:`~post_reply`
    along with any messages that were captured while it was
    executing. The command is removed from internal
    list and a message is computed and sent.

    The side that initiated the command receives the message
    in :meth:`~process_reply`, where the result is associated
    with the initial message and saved.

    All this time the caller pools the status by calling :meth:`~get_reply`.
    When it finally returns the result it also removes
    the command from internal list.

    .. note:
       There are two `Message` classes used in this implementation:
       one is provided by the p2p0mq library as a bucket for
       transportation and the other one is provided by this library
       and groups stuff for the user to see or use (
       errors, warnings, information).

    Attributes:
        encoder (SerDeSer):
            Used to convert commands to and from bytes.
        provider (RemoteProvider):
            Used on the receiving side as a destination for the command.
        sent_messages (dict):
            On the caller side holds the messages that were sent and which
            don't have a reply, yet. The keys are message ids and values
            are tuples of three values:

            * the message that was sent
            * the command that was sent
            * `None` in initial step, list of messages that resulted, later.

        received_commands (dict):
            On the receiver side holds the messages and commands that were
            received and for which we haven't sent a reply back, yet.
            The keys are command ids and values are tuples of three values:

            * the message that was received
            * the command that was decoded from the message
            * the reply message that will be updated once the command completes.
    """

    def __init__(self, encoder, provider, *args, **kwargs):
        """
        Constructor.

        Arguments:
            encoder (SerDeSer):
                Used to convert commands to and from bytes.
            provider (RemoteProvider):
                Used on the receiving side as a destination for the command.
        """
        super().__init__(name="terminal", command_id=b'et', *args, **kwargs)
        self.encoder = encoder
        self.provider = provider
        self.sent_messages = {}
        self.received_commands = {}

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'RemoteConcern()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'RemoteConcern()'

    def compose(self, peer, command):
        """
        Creates a message for a command and stores the message.

        Arguments:
            peer (Peer):
                The host where we want to send the message.
            command (Command):
                The command or request to send.
        Returns:
            p2p0mq.message.Message:
                The message to send.
        """
        message = Message(
            source=self.app.uuid,
            to=peer.uuid,
            previous_hop=None,
            next_hop=peer.uuid if peer.state_connected else peer.via,
            command=self.command_id,
            reply=False,
            handler=self,
            command_content=self.encoder.pack_command(command)
        )
        assert message.valid_for_send(self.app)
        self.sent_messages[message.message_id] = (message, command, None)
        return message

    def process_request(self, message):
        """
        Called when we receive a command or request.

        The method decodes the command, stores it along with the message and
        posts the command to the provider.

        Arguments:
            message (p2p0mq.message.Message):
                The packed message that we decode here.
        """
        command = self.encoder.unpack_command(
            message.payload['command_content'])
        self.received_commands[command.uuid] = (
            message, command, message.create_reply())
        self.provider.enqueue_command(command)

    def post_reply(self, command, messages):
        """
        Called when a command completes its execution to send the reply back.

        The command completes the reply message and sends it to the requester.

        Arguments:
            command (Command):
                The command that was executed. Note that this might not be
                the same object as the one that was received.
            messages (list of enhterm.message.Message):
                Messages generated while the command was executed.
        """
        try:
            initial_message, saved_command, reply = \
                self.received_commands[command.uuid]
        except KeyError:
            logger.error(
                "Post reply for a command we haven't seen: %r", command)
            return
        del self.received_commands[command.uuid]
        reply.payload['result'] = self.encoder.pack_result(command, messages)
        self.provider.zmq_app.sender.medium_queue.enqueue(reply)

    def process_reply(self, message):
        """
        Called when a reply message finally arrives.

        We only process messages that we know about.

        Arguments:
            message (p2p0mq.message.Message):
                The message that arrived.
        """
        try:
            local_message, command, reply = self.sent_messages[message.message_id]
        except KeyError:
            logger.error("Got reply for a message we haven't send: %r", message)
            return

        if reply is None:
            class_id, uuid, result, messages = self.encoder.unpack_result(
                message.payload['result'])
            self.sent_messages[message.message_id] = (
                local_message, command, messages)
            command.result = result
            logger.log(TRACE, "Got reply %r for %r", message, local_message)
        else:
            logger.error("Got reply %r for %r; we already have a reply: %r",
                         message, local_message, reply)

    def get_reply(self, message, remove_on_success=True):
        local_message, command, messages = self.sent_messages[message.message_id]
        if messages is not None:
            if remove_on_success:
                del self.sent_messages[message.message_id]
            return command, messages
        else:
            return None
