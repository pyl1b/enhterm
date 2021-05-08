# -*- coding: utf-8 -*-
"""
Contains the definition of the RemoteProvider class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from enhterm.impl.p2p.p2p_watcher import RemoteWatcher
from enhterm.provider.queue_provider import QueueProvider

logger = logging.getLogger('RemoteProvider')


class RemoteProvider(QueueProvider):
    """
    Provider that waits for remote commands and can cache them.

    The purpose of a provider is to give commands to be executed
    in response to :meth:`~get_command` method. This provider is
    based on the :class:`~QueueProvider` which can accumulate
    commands and issue them in the order of their arrival
    and can also block when there are no commands.

    The constructor also creates an associated :class:`~RemoteWatcher`
    that the user is expected to install into the terminal.

    This class might not be useful as it is, since the
    :class:`~RemoteRunner` sends :class:`~TextCommand` in its
    default incarnation. See
    :class:`~enhterm.provider.parser.argparser.ArgparseRemoteProvider`
    for an implementation that parses the text.

    Attributes:
        zmq_app (LocalPeer):
            The zmq interface used for communication.
    """

    def __init__(self, zmq_app, *args, **kwargs):
        """
        Constructor.

        Arguments:
            zmq_app (LocalPeer):
                The zmq interface used for communication.
        """
        self.zmq_app = zmq_app
        self.watcher = RemoteWatcher(provider=self)
        super().__init__(*args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'RemoteProvider()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'RemoteProvider()'

    @property
    def concern(self):
        """
        Get the concern that mediates message transport.

        It is asserted that the :class:`~LocalPeer` installed in the instance
        has a concern which exports the `et` message type.
        """
        return self.zmq_app.concerns[b'et']
