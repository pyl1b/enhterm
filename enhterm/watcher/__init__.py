# -*- coding: utf-8 -*-
"""
Contains the definition of the Watcher class.
"""
import logging

logger = logging.getLogger('et.w')


class Watcher(object):
    """
    A base class for structures informed by the terminal about its events.

    The user will subclass this class and implement the methods, then will
    simply append an instance to the terminal:

    >>> from enhterm import EnhTerm
    >>> from enhterm.watcher import Watcher
    >>> term = EnhTerm()
    >>> watcher = Watcher()
    >>> term.watchers.append(watcher)

    Attributes:
        term (EnhTerm):
            The terminal that is being monitored.
    """

    def __init__(self, term=None, *args, **kwargs):
        """
        Constructor.

        Arguments:
            term (EnhTerm)
                The terminal that is serviced by this watcher.
        """
        super().__init__(*args, **kwargs)
        self.term = term

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'Watcher()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'Watcher()'

    def pre_loop(self):
        """
        The watcher is informed that the terminal entered the command loop.
        """
        pass

    def post_loop(self):
        """
        The watcher is informed that the terminal is exiting the command loop.
        """
        pass

    def pre_cmd(self, command):
        """
        The watcher is informed that the terminal is about to execute a command.

        Arguments:
            command (Command):
                The command to be executed.
        """
        pass

    def post_cmd(self, command):
        """
        The watcher is informed that the terminal has executed a command.

        At this point the result is set in the command structure.

        Arguments:
            command (Command):
                The command that was executed.
        """
        pass

    def message_issued(self, message):
        """
        The watcher is informed that the terminal has issued a message.

        Arguments:
            message (Message):
                The message that was issued.
        """
        pass
