# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

from . import HelperShell

logger = logging.getLogger('test.enhterm')


class TestEnhTermMacros:

    def setup(self):
        self.testee = HelperShell()

    def teardown(self):
        self.testee.postloop()

    def test_run_macro(self):
        self.testee.commandme("run macro")
        self.testee.assert_name()
        self.testee.clear_saved_messages()

        self.testee.commandme("run macro nonexistent1 nonexistent2")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.unknown_argument_helper('nonexistent2')
        self.testee.clear_saved_messages()

        self.testee.commandme("run macro nonexistent")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.assert_has_error('does not exist')
        self.testee.assert_has_error('nonexistent')
        self.testee.clear_saved_messages()

        self.testee.commandme("new macro nonexistent")
        self.testee.assert_msg(errors=0, warnings=0, info=0)
        self.testee.commandme("run macro nonexistent2")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.assert_has_error('does not exist')
        self.testee.assert_has_error('nonexistent2')
        self.testee.clear_saved_messages()
        self.testee.commandme("end macro")
        self.testee.commandme("drop macro nonexistent")
        self.testee.commandme("new macro nonexistent")
        self.testee.commandme("end macro")
        self.testee.assert_msg(errors=0, warnings=0, info=0)
        self.testee.commandme("run macro nonexistent1 nonexistent2")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.unknown_argument_helper('nonexistent2')
        self.testee.clear_saved_messages()
        self.testee.commandme("run macro nonexistent")
        self.testee.assert_msg(errors=0, warnings=0, info=0)
        self.testee.clear_saved_messages()

        self.testee.assert_has_help("run macro")


    def test_drop_macro(self):
        self.testee.commandme("drop macro")
        self.testee.assert_name()
        self.testee.clear_saved_messages()

        self.testee.commandme("drop macro nonexistent")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.assert_has_error('does not exist')
        self.testee.assert_has_error('nonexistent')
        self.testee.clear_saved_messages()

        self.testee.commandme("drop macro nonexistent1 nonexistent2")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.unknown_argument_helper('nonexistent2')
        self.testee.clear_saved_messages()

        self.testee.commandme("new macro nonexistent")
        self.testee.assert_msg(errors=0, warnings=0, info=0)
        self.testee.commandme("drop macro nonexistent")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.assert_has_error('does not exist')
        self.testee.assert_has_error('nonexistent')
        self.testee.clear_saved_messages()
        self.testee.commandme("end macro nonexistent")
        self.testee.unknown_argument_helper('nonexistent')
        self.testee.clear_saved_messages()
        self.testee.commandme("end macro")
        self.testee.assert_msg(errors=0, warnings=0, info=0)
        self.testee.commandme("drop macro nonexistent1 nonexistent2")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.unknown_argument_helper('nonexistent2')
        self.testee.clear_saved_messages()
        self.testee.commandme("drop macro nonexistent")
        self.testee.assert_msg(errors=0, warnings=0, info=0)
        self.testee.clear_saved_messages()

        self.testee.assert_has_help("drop macro")

    def test_list_macros(self):
        self.testee.commandme("list macros abcdef 123456")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.assert_has_error('Too many arguments for command')
        self.testee.clear_saved_messages()

        self.testee.commandme("list macros abcdef")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.assert_has_error('Invalid argument for command')
        self.testee.clear_saved_messages()

        def no_macros():
            self.testee.assert_msg(errors=0, warnings=0, info=1)
            self.testee.assert_has_info('MACROS')
            self.testee.assert_has_info('No macros have been defined')
            self.testee.clear_saved_messages()

        self.testee.commandme("list macros")
        no_macros()
        self.testee.commandme("list macros true")
        no_macros()
        self.testee.commandme("list macros false")
        no_macros()

        self.testee.commandme("new macro aftershock")
        self.testee.commandme("end macro")

        def has_aftershock():
            self.testee.assert_msg(errors=0, warnings=0, info=1)

            self.testee.assert_has_info('aftershock')
            self.testee.clear_saved_messages()

        self.testee.commandme("list macros")
        has_aftershock()
        self.testee.commandme("list macros true")
        self.testee.assert_not_info('new macro aftershock')
        has_aftershock()
        self.testee.commandme("list macros false")
        has_aftershock()

        self.testee.assert_has_help("list macros")

    def test_end_macro(self):
        self.testee.commandme("end macro")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.assert_has_error('Not recording a macro')
        self.testee.clear_saved_messages()

        self.testee.commandme("end macro abcd")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.unknown_argument_helper('abcd')
        self.testee.clear_saved_messages()

        self.testee.commandme("new macro abcd")
        self.testee.commandme("end macro abcd")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.unknown_argument_helper('abcd')
        self.testee.clear_saved_messages()

        self.testee.commandme("end macro")
        self.testee.assert_msg(errors=0, warnings=0, info=0)

        self.testee.assert_has_help("end macro")

    def test_new_macro(self):
        self.testee.commandme("new macro abcd efghij")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.unknown_argument_helper('efghij')
        self.testee.clear_saved_messages()

        self.testee.commandme("new macro")
        self.testee.assert_name()
        self.testee.clear_saved_messages()

        self.testee.commandme("new macro abcd")
        self.testee.assert_msg(errors=0, warnings=0, info=0)
        self.testee.clear_saved_messages()
        self.testee.commandme("end macro")
        self.testee.assert_msg(errors=0, warnings=0, info=0)

        self.testee.assert_has_help("new macro")


if __name__ == '__main__':
    import nose
    nose.runmodule()
