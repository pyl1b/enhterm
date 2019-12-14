# -*- coding: utf-8 -*-
"""
Contains the definition of the RemoteRunner class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from time import sleep

from p2p0mq.peer import Peer

from enhterm.runner import Runner

logger = logging.getLogger('et.runrem')


class RemoteRunner(Runner):
    """
    A runner that sends all commands to a remote host.

    The remote host will execute the command, capture the output and
    will send it back here.

    Attributes:

    """

    def __init__(self, zmq_app, timeout=4, peer=None, *args, **kwargs):
        """
        Constructor.

        Arguments:
            zmq_app (LocalPeer):
                The zmq interface used for communication.
            timeout (int):
                Seconds to wait for the reply.
            peer (Peer or type or str):
                Can be either a :class:`Peer` instance or a peer id (in
                this case the `zmq_app` is required as it will be searched
                for in it).
        """
        self.zmq_app = zmq_app
        self.timeout = timeout
        if (not isinstance(peer, Peer)) and (peer is not None):
            peer = self.zmq_app.peers[peer]
        self.peer = peer
        super().__init__(*args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'RemoteRunner()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'RemoteRunner()'

    def __call__(self, command):
        """
        Execute the command.

        Arguments:
            command (Command):
                The command to execute.
        """

        # Create and post a message.
        message = self.concern.compose(peer=self.peer, command=command)
        self.zmq_app.medium_queue.enqueue(message)

        # Wait for it to return.
        for i in range(self.timeout*2):
            reply = self.concern.get_reply(message)
            if reply is not None:
                break
            sleep(0.5)
        else:
            self.timed_out()
            return None

        # Print all messages captured on the remote.
        for message in reply.messages:
            self.term.issue_message(message)

        # And return the result provided by the remote.
        return reply.result

    @property
    def concern(self):
        """ Get the concern that mediates message transport. """
        return self.zmq_app.concerns[b'et']

    def timed_out(self):
        raise TimeoutError
