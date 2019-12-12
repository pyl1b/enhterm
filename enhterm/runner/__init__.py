# -*- coding: utf-8 -*-
"""
Contains the definition of the Runner  class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

logger = logging.getLogger('Runner ')


class Runner(object):
    """
    The class that receives the command and performs some
    actions with it.

    Default implementation calls simply calls the
    :meth:`~enhterm.command.Command.execute` method of the
    :class:`~enhterm.command.Command`.

    Attributes:
        term (EnhTerm):
            The terminal where this runner performs.
    """

    def __init__(self, term=None, *args, **kwargs):
        """
        Constructor.

        Arguments:
            term (EnhTerm):
                The terminal where this runner performs.
        """
        self.term = term
        super().__init__(*args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'Runner ()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'Runner ()'

    def __call__(self, command):
        """
        Execute the command.

        Arguments:
            command (Command):
                The command to execute.
        """
        return command.execute()
