# -*- coding: utf-8 -*-
"""
Contains the definition of the RemoteRunner class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from time import sleep

from p2p0mq.peer import Peer

from enhterm.command.text import TextCommand
from enhterm.runner import Runner

logger = logging.getLogger('et.runrem')


class RemoteRunner(Runner):
    """
    A runner that sends all text commands to a remote host.

    The purpose of the runner is to take commands and do something useful
    with them. The default runner simply executes the command by calling
    its :meth:`Command.execute` method. This runner takes the command
    and sends it as a message to a remote host.

    The remote host will execute the command, capture the output and
    will send it back here. The output consists of the command
    result and the list of messages that were generated since command
    started to execute and until it ended (:class:`~RemoteWatcher` is used
    for that on the remote host.

    The runner waits for the result and issues the messages as if they were
    generated on this host and returns the result of running the command.
    The result is also stored inside the command that was provided as input.

    Attributes:
        zmq_app (LocalPeer):
            The structure where we post our messages.
        timeout (int):
            Seconds to wait for the reply.
        peer (Peer or type or str):
            Can be either a :class:`Peer` instance or a peer id (in
            this case the `zmq_app` is required as it will be searched
            for in it).
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

        The call only sends :class:`~TextCommand' and its subclasses.
        Any other command is executed by calling its
        `meth`:~Command.execute` method and the result is returned directly.

        The :class:`~RemoteConcern` class is used to construct a message
        from the command
        then we place the message in the queue and wait for a result for a
        certain number of seconds decided by the `timeout` member.

        In case of timeout the :meth:`~timed_out` method is called
        (which raises a :class:`TimeoutError` by default) and `None`
        is returned.

        The :class:`~RemoteConcern` returns the messages that were
        issued while running the command, and which are re-issued in
        this context. The result of the call is the result of the
        command in the remote context.

        Arguments:
            command (Command):
                The command to execute.
        """
        if not isinstance(command, TextCommand):
            return command.execute()

        # Create and post a message.
        message = self.concern.compose(peer=self.peer, command=command)
        self.zmq_app.sender.medium_queue.enqueue(message)

        # Wait for it to return.
        for i in range(int(self.timeout*2)):
            reply = self.concern.get_reply(message)
            if reply is not None:
                break
            sleep(0.5)
        else:
            self.timed_out()
            return None

        sent_command, messages = reply
        assert sent_command == command

        # Print all messages captured on the remote.
        if messages is not None:
            for message in messages:
                self.term.issue_message(message)

        # And return the result provided by the remote.
        return sent_command.result

    @property
    def concern(self):
        """
        Get the concern that mediates message transport.

        It is asserted that the :class:`~LocalPeer` installed in the instance
        has a concern which exports the `et` message type.
        """
        return self.zmq_app.concerns[b'et']

    def timed_out(self):
        """
        Called when executing a command takes longer than anticipated.

        Default implementation raises a :class:TimeoutError`
        exception. Re-implement it to do something else.

        It is safe for the function to return
        (:meth:`__call__` returns `None` in that case).
        """
        raise TimeoutError
