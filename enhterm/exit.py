# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

logger = logging.getLogger('enhterm')


class ExitMixin(object):
    """
    Provides the exit command.
    """
    def __init__(self, *args, **kwargs):
        super(ExitMixin, self).__init__(*args, **kwargs)

    def do_exit(self, arg):
        """Terminate all agents and exit the interactive prompt"""
        return True
