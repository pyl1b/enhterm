# -*- coding: utf-8 -*-
"""
Contains the definition of the Provider class.
"""
import logging

from enhterm.base import EtBase

logger = logging.getLogger('et.p')


class Provider(EtBase):
    """
    A class capable of providing command to the terminal.

    To install the

    Attributes:
        term (EnhTerm):
            The terminal that is serviced by this provider.
            :meth:`~EnhTerm.install_provider` and
            :meth:`~EnhTerm.uninstall_provider` will change this value.
    """

    def __init__(self, term=None, *args, **kwargs):
        """
        Constructor.

        Arguments:
            term (EnhTerm)
                The terminal that is serviced by this provider.
                :meth:`~EnhTerm.install_provider` will overwrite this value.
        """
        super().__init__(*args, **kwargs)
        self.term = term

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'Provider()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'Provider()'

    def start(self, other):
        """
        The provider is informed that it is the active provider.

        This method is called when the provider has been installed into
        the terminal and just before it is made the top provider.

        An exception in this method will cause the install procedure
        to fail and the provider will not be added to the stack.

        Arguments:
            other (Provider or None):
                The previous top provider that we're replacing as
                active provider.
        """
        pass

    def stop(self):
        """
        The provider is informed that it was uninstalled.

        The uninstall can be triggered by the provider, by returning a `None`
        command when asked to, or by an exception in the provider.
        """
        pass

    def pause(self, other):
        """
        The provider is informed that it is no longer the top provider.

        An exception in this method will cause terminal to uninstall
        the provider.

        Arguments:
            other (Provider or None):
                The provider that is being installed.
        """
        pass

    def unpause(self):
        """
        The provider is informed that it is the top provider, again.

        An exception in this method will cause terminal to uninstall
        the provider.
        """
        pass

    def get_command(self):
        """
        Retrieve next command to execute.

        This method is only called when the provider is the active one.

        Returns:
            Command or None
                The function must return either a command instance or None,
                in which case the provider will be uninstalled.
        """
        raise NotImplementedError
