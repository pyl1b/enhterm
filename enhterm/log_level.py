# -*- coding: utf-8 -*-
"""
Allow the user to control the level of logging.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from .lang import _


logger = logging.getLogger('enhterm')


class LogLevelMixin(object):
    args_set_loglevel = ['level', 'args']

    def __init__(self, *args, **kwargs):
        super(LogLevelMixin, self).__init__(*args, **kwargs)
        self.add_subcommand('set', 'loglevel')

    def sdo_set_loglevel(self, arg):
        command_format = _(
            "The format of the command is `set loglevel LEVEL [[to] TARGET]`\n"
            "Where LEVEL is `d[ebug]` , `i[nfo]`, `w[arning]` and `e[rror]` \n"
            "TARGET is one of `c[onsole]` or `f[ile]` (default is console)")
        console_handler = None
        file_handler = None
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                file_handler = handler
            elif isinstance(handler, logging.StreamHandler):
                console_handler = handler

        def get_kind(value):
            kind = value.lower()
            if kind in ('c', 'con', 'console'):
                target = (console_handler, 'console')
            elif kind in ('f', 'file'):
                target = (file_handler, 'file')
            else:
                self.error(_("Invalid target argument: %s") % kind,
                           command_format)
                target = (None, None)
            return target

        target = None
        target_str = ''
        log_level = None
        level_str = arg['level'].lower()
        args = arg['args']

        if len(args) == 0:
            target = console_handler
            target_str = 'console'
        elif len(args) == 1:
            target, target_str = get_kind(args[0])
        elif len(args) == 2:
            sugar = args[0].lower()
            if not sugar in ('2', 'to'):
                self.error(_("Invalid list of arguments"), command_format)
            else:
                target, target_str = get_kind(args[1])
        else:
            self.error(_("Invalid list of arguments"), command_format)

        if level_str in ('d', 'debug'):
            log_level = logging.DEBUG
        elif level_str in ('w', 'warn', 'warning'):
            log_level = logging.WARNING
        elif level_str in ('i', 'info', 'information'):
            log_level = logging.INFO
        elif level_str in ('e', 'err', 'error'):
            log_level = logging.ERROR
        elif level_str in ('c', 'crit', 'critical'):
            log_level = logging.CRITICAL
        else:
            try:
                log_level = int(level_str)
            except ValueError:
                self.error(_("Invalid level"), command_format)

        if not (log_level is None or target is None):
            target.setLevel(log_level)
            top_log = logging.getLogger()
            if top_log.level > log_level:
                top_log.setLevel(log_level)
            logger.debug('New log level %s set to %s', level_str, target_str)

    def helps_set_loglevel(self):
        self.info(_("""Change logging verbosity.

Arguments
---------
level:    new level; can be one of `d[ebug]` , `i[nfo]`, 
          `w[arning]` or `e[rror]`
to:       this is just syntactic sugar so the sentence looks nice; 
          can be omitted;
adapter:  the adapter(s) that should receive the words.

Description
-----------
The program logs data to a file and to console. The user can control the 
verbosity by using this command.

Please note that there are two notification systems:
- the logging system is mostly used by the library and low level commands;
- the command system uses a separate way of printing errors only to 
the screen.
This command controls the low level logging facility.

Example
-------
$: set loglevel debug to console
$: set loglevel debug console
$: set loglevel d c
$: set loglevel debug
$: set loglevel info to file
$: set loglevel i f
"""))
