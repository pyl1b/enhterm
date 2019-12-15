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
    This class .

    Attributes:

    """

    def __init__(self, encoder, provider, *args, **kwargs):
        """
        Constructor.

        Arguments:

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
        command = self.encoder.unpack_command(
            message.payload['command_content'])
        self.received_commands[command.uuid] = (
            message, command, message.create_reply())
        self.provider.enqueue_command(command)

    def post_reply(self, command, messages):
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
        try:
            local_message, command, reply = self.sent_messages[message.message_id]
        except KeyError:
            logger.error("Got reply for a message we haven't send: %r", message)
            return

        if reply is None:
            class_id, uuid, result, messages = self.encoder.unpack_result(
                message.payload['result'])
            self.sent_messages[message.message_id] = (local_message, command, messages)
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
