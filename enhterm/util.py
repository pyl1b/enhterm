# -*- coding: utf-8 -*-
"""
"""
from __future__ import print_function
from __future__ import unicode_literals

import logging

logger = logging.getLogger('enhterm')


from .lang import _


def needs_name(original_function):
    """Decorator that extracts the name argument."""
    def new_function(self, arg):
        name = arg['name'].strip()
        if len(name) == 0:
            self.error(_("A name needs to be provided"))
            return
        return original_function(self, arg, name)
    return new_function
