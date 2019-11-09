# -*- coding: utf-8 -*-
"""
Generic enhanced terminal command loop.
"""
from __future__ import unicode_literals
from __future__ import print_function

import cmd
import logging

from .command import CommandMixin
from .exit import ExitMixin
from .help import HelpMixin
from .macro import MacroMixin
from .message import MessagesMixin
from .run_command import RunCommandsMixin
from .subcommand import SubcommandMixin
from .log_level import LogLevelMixin
from .lang import _

logger = logging.getLogger('enhterm')


class EnhTerm(MessagesMixin, ExitMixin, HelpMixin,
              CommandMixin, SubcommandMixin,
              MacroMixin, RunCommandsMixin,
              LogLevelMixin, cmd.Cmd):
    """
    Enhanced terminal.

    This is a base class you can use in your project to create a command loop.
    It includes all mixins defined by the package. If you need fewer
    mixins use this class as a template.
    """
    shortcuts = {'x': ('exit', '')}

    def __init__(self, *args, **kwargs):
        self.intro = _('Welcome to the interactive shell.   '
                       'Type help or ? to list commands.\n')
        super(EnhTerm, self).__init__()
        cmd.Cmd.__init__(self, *args, **kwargs)
        self.prompt = '$: '

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.
        """
        should_exit, result = self.cmd_with_result(line)
        MacroMixin.command_hook(self, line)
        return should_exit

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt."""
        pass

