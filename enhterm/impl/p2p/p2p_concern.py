# -*- coding: utf-8 -*-
"""
Contains the definition of the RemoteConcern class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from p2p0mq.concerns.base import Concern
from p2p0mq.message import Message

logger = logging.getLogger('RemoteConcern')


class RemoteConcern(Concern):
    """
    This class .

    Attributes:

    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Arguments:

        """
        super().__init__(name="terminal", command_id=b'et', *args, **kwargs)

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
            command_content=command.encode()
        )
        assert message.valid_for_send(self.app)
        return message

    def process_request(self, message):
        pass

    def process_reply(self, message):
        pass
