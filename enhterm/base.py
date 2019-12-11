# -*- coding: utf-8 -*-
"""
Contains the definition of the EtBase class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

logger = logging.getLogger('EtBase')


class EtBase(object):
    """
    Base class for all classes in this library
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Arguments:

        """
        assert len(args) == 0, f"Unhandled positional arguments: {args}"
        assert len(kwargs) == 0, f"Unhandled keyword arguments: {kwargs}"
        super().__init__()

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'EtBase()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'EtBase()'
