# -*- coding: utf-8 -*-
"""
Contains the definition of the QueueProvider class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from enhterm.mixins.queued import QueueMixin
from enhterm.provider import Provider

logger = logging.getLogger('et.q')


class QueueProvider(QueueMixin, Provider):
    """
    A provider that can store and issue commands.

    If `block` is true and `timeout` is `None` (the default),
    block if necessary until an item is available. If `timeout` is
    a non-negative number, it blocks at most `timeout` seconds.

    If `block` is `False` return a :class:`~Command` if one is immediately
    available ('timeout' is ignored in that case).

    If a :class:`~Command` is not present in the queue the provider
    either uninstalls itself by returning `None` or returns the command
    defined in `on_empty` attribute (:class:`NoOpCommand` by default).

    Attributes:
        block (bool):
            Should the queue wait for a command or return immediately?
        timeout (float):
            The time to block, waiting for an item.
        on_empty (None or callable):
            If `None` the provider will return None on :meth:`~get_command`,
            causing the terminal to uninstall the provider.
            Otherwise the provider will call this member in order
            to construct the command. The constructor sets this attribute
            to either `None` or :class:`NoOpCommand`.

    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Arguments:
            block (bool):
                Should the queue wait for a command or return immediately?
            timeout (float):
                The time to block, waiting for an item.
            close_on_empty (bool):
                If `True` the provider will return None on :meth:`~get_command`,
                causing the terminal to uninstall the provider.
                If `False` the provider will construct a command from the
                `on_empty` attribute (:class:`NoOpCommand` by default).
        """
        super().__init__(*args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'QueueProvider()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'QueueProvider()'

