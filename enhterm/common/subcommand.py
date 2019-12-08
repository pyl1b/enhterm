# -*- coding: utf-8 -*-
"""
"""
from __future__ import print_function
from __future__ import unicode_literals

import logging

from enhterm.lang import _

logger = logging.getLogger('enhterm')


class SubcommandMixin(object):
    """
    Infrastructure for sub-commands.
    """
    subcommands = {}

    def __init__(self, *args, **kwargs):
        super(SubcommandMixin, self).__init__(*args, **kwargs)

    def add_subcommand(self, command, subcommand, callable=None):
        """
        Add a sub-command.

        Arguments:
            command (string or list) :
                Can be either a path or a single string
                (will be converted in a path with a single element).
            subcommand (string) :
                The final element of the path.
            callable (string) :
                The name of the function to call.
        """
        if not isinstance(command, (list, set, tuple)):
            command = (command, )

        the_store = self.subcommands
        traceme = ''
        for item in command:
            try:
                dive = the_store[item]
            except KeyError:
                dive = {}
                the_store[item] = dive
            traceme = '%s_%s' % (traceme, item) if len(traceme) else item
            the_store = dive

        # we can compute this ourselves.
        if callable is None:
            callable = '%s_%s' % (traceme, subcommand)

        try:
            the_store[subcommand] = callable
        except KeyError:
            the_store[subcommand] = {subcommand: callable}

    def get_subcommand(self, command, args):

        missing_is_error = False
        traceme = ''
        the_store = self.subcommands

        while True:

            traceme = '%s_%s' % (traceme, command) if len(traceme) else command

            # first level generates KeyError if the command is not found
            # other levels generate RuntimeError
            try:
                subcommands = the_store[command]
            except KeyError as exc:
                if missing_is_error:
                    raise RuntimeError(_("Command <%s> is not defined") % traceme)
                else:
                    raise exc

            # subcommands is a dict of commands names
            # if this is a nested list
            # of a function name
            if isinstance(subcommands, str):
                return subcommands, args
            the_store = subcommands

            if len(args) == 0:
                raise RuntimeError(_("Command <%s> needs a subcommand") % traceme)

            command, args, line = self.parseline(args)

    def print_subcommands(self):
        """Informs the user about available subcommands."""
        def recursive(indent, value):
            for kkk in value:
                self.info_line("%s%s" % (indent, kkk))
                new_val = value[kkk]
                if not isinstance(new_val, str):
                    recursive(indent + '  ', new_val)

        recursive('', self.subcommands)
