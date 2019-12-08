# -*- coding: utf-8 -*-
"""
"""
from __future__ import print_function
from __future__ import unicode_literals

import cmd
import logging

from enhterm.lang import _

logger = logging.getLogger('enhterm')


class HelpMixin(object):
    """
    Extends normal help command output.
    """
    def __init__(self, *args, **kwargs):
        super(HelpMixin, self).__init__(*args, **kwargs)

    def do_help(self, arg):
        """
        List available commands with "help" or detailed help with "help cmd".
        """

        def help_attempt(name, tag_help='help_', tag_do='do_'):
            try:
                func = getattr(self, tag_help + name)
                # print ("has help")
            except AttributeError:
                # print ("no help")
                try:
                    doc = getattr(self, tag_do + name).__doc__
                    # print("has do")
                    if doc:
                        self.print_message("%s\n" % str(doc))
                        return True
                except AttributeError:
                    # print("no do")
                    pass
                return False
            func()
            return True

        if arg:
            if not help_attempt(arg):
                if not help_attempt(
                        arg.replace('  ', ' ').replace(' ', '_'),
                        tag_help='helps_',
                        tag_do='sdo_'):
                    self.print_message("%s\n" % str(self.nohelp % (arg,)))
        else:
            # noinspection PyCallByClass
            cmd.Cmd.do_help(self, arg)
        if len(arg) == 0:
            if len(self.subcommands) > 0:
                self.info_start(_("SUB-COMMANDS:\n"
                                  "============"))
                self.print_subcommands()
                self.info_end(_("\n\n"))
            if len(self.shortcuts) > 0:
                self.info_start(_("SHORTCUTS:\n"
                                  "=========="))
                for k in self.shortcuts:
                    self.info_line(_("   %-16s  %s") % (
                        k, ' '.join(self.shortcuts[k])))
                self.info_end(_(""))
            try:
                getattr(self, 'help_getting_started')
                self.info(_("Type 'help getting started' to see a "
                            "step-by-step introduction"))
            except AttributeError:
                pass
