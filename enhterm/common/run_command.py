# -*- coding: utf-8 -*-
"""
"""
from __future__ import print_function
from __future__ import unicode_literals

import logging

logger = logging.getLogger('enhterm')


class RunCommandsMixin(object):
    """
    Sequence of commands.
    """
    def __init__(self, *args, **kwargs):
        super(RunCommandsMixin, self).__init__(*args, **kwargs)

    def run_commands(self, commands):
        """
        Run a sequence of commands.

        Line starting with a # character are ignored (comments).
        """
        if isinstance(commands, str):
            commands = commands.split('\n')
        for cmditer in commands:
            if cmditer.strip().startswith("#"):
                continue
            should_exit, result = self.cmd_with_result(cmditer)
            if not result:
                break

    def run_file(self, fpath):
        """Executes a file (expects UTF-8 encoding."""
        with open(fpath, "r", encoding="utf-8") as fin:
            return self.run_commands(fin.read())

    args_exec = ['path']

    def do_exec(self, arg):
        """
        Executes the commands in a file.

        Parameters
        ----------

        path : string
            The path to a file to execute.
        """
        self.run_file(arg['path'])

