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
    Provider that waits for remote commands and can cache them

    Attributes:

    """

    def __init__(self, zmq_app, *args, **kwargs):
        """
        Constructor.

        Arguments:

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
        """ Get the concern that mediates message transport. """
        return self.zmq_app.concerns['terminal']
