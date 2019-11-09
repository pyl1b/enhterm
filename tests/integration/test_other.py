# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import os
import tempfile

from nose.tools import (
    assert_equal,
    assert_equals,
    assert_false,
    assert_is_none,
    assert_true,
)

from tests.integration import HelperShell

logger = logging.getLogger('test.enhterm')


class TestEnhTerm:

    def setup(self):
        self.tmp_log = tempfile.mktemp()
        self.testee = HelperShell()
        self.top_log = logging.getLogger()

        self.console_handler = logging.StreamHandler()
        self.file_handler = logging.FileHandler(self.tmp_log)
        self.top_log.addHandler(self.console_handler)
        self.top_log.addHandler(self.file_handler)
        self.clear_log_state()

    def clear_log_state(self, to_level=logging.CRITICAL):
        self.top_log.setLevel(to_level)
        self.console_handler.setLevel(to_level)
        self.file_handler.setLevel(to_level)
        self.testee.clear_saved_messages()

    def teardown(self):
        self.testee.postloop()
        self.file_handler.close()
        if os.path.isfile(self.tmp_log):
            os.remove(self.tmp_log)
        self.top_log.removeHandler(self.console_handler)
        self.top_log.removeHandler(self.file_handler)

    def test_exit(self):
        assert_false(self.testee.stop)
        self.testee.commandme("exit")
        self.testee.assert_msg(errors=0, warnings=0, info=0)
        assert_true(self.testee.stop)
        self.testee.postloop()
        self.testee.clear_saved_messages()

    def test_help(self):
        assert_false(self.testee.stop)
        self.testee.commandme("help")
        assert_is_none(self.testee.stop)
        self.testee.postloop()
        self.testee.assert_msg(errors=0, warnings=0, info=2)
        self.testee.assert_has_info('SUB-COMMANDS')
        self.testee.assert_has_info('SHORTCUTS')
        self.testee.clear_saved_messages()

    def test_exec(self):
        assert_equals(self.testee.error_count, 0)
        self.testee.commandme("exec")
        assert_equals(self.testee.error_count, 1)
        self.testee.clear_saved_messages()

        with tempfile.TemporaryDirectory() as d:
            temp_file_name = os.path.join(d, 'your_temp_file.name')
            with open(temp_file_name, "w") as fout:
                fout.write("help\nexit")
            self.testee.commandme("exec %s" % temp_file_name.replace("\\", "/"))
            assert_equals(self.testee.error_count, 0)
            assert_equals(self.testee.warning_count, 0)
            assert_equals(self.testee.info_count, 2)
            self.testee.assert_has_info('SUB-COMMANDS')
            self.testee.assert_has_info('SHORTCUTS')
        self.testee.clear_saved_messages()

    def test_run(self):
        self.testee.needs_subcommand_helper("run")

    def test_drop(self):
        self.testee.needs_subcommand_helper("drop")

    def test_list(self):
        self.testee.needs_subcommand_helper("list")

    def test_end(self):
        self.testee.needs_subcommand_helper("end")

    def test_new(self):
        self.testee.needs_subcommand_helper("new")

    def helper_log(self, lvl, level, trg, target,
                   expect_t, expect_c, expect_f):
        def herehere(lvl, trg):
            self.clear_log_state()
            self.testee.commandme("set loglevel %s %s" % (lvl, trg))
            self.testee.assert_msg(errors=0, warnings=0, info=0)
            assert_equal(self.top_log.level, expect_t)
            assert_equal(self.console_handler.level, expect_c)
            assert_equal(self.file_handler.level, expect_f)

            self.clear_log_state()
            self.testee.commandme("set loglevel %s to %s" % (lvl, trg))
            self.testee.assert_msg(errors=0, warnings=0, info=0)
            assert_equal(self.top_log.level, expect_t)
            assert_equal(self.console_handler.level, expect_c)
            assert_equal(self.file_handler.level, expect_f)

            self.clear_log_state()
            self.testee.commandme("set loglevel %s 2 %s" % (lvl, trg))
            self.testee.assert_msg(errors=0, warnings=0, info=0)
            assert_equal(self.top_log.level, expect_t)
            assert_equal(self.console_handler.level, expect_c)
            assert_equal(self.file_handler.level, expect_f)

        herehere(lvl, trg)
        herehere(lvl, target)
        herehere(level, trg)
        herehere(level, target)

    def test_log_level_positive(self):
        self.testee.assert_has_help("set loglevel")

        def herehere(particle, long_form=None, expect=None):
            if not long_form:
                long_form = particle
            if not expect:
                expect = particle

            self.clear_log_state()
            self.testee.commandme("set loglevel %s" % particle)
            self.testee.assert_msg(errors=0, warnings=0, info=0)
            assert_equal(self.top_log.level, expect)
            assert_equal(self.console_handler.level, expect)
            assert_equal(self.file_handler.level, logging.CRITICAL)
            self.clear_log_state()
            self.testee.commandme("set loglevel %s" % long_form)
            self.testee.assert_msg(errors=0, warnings=0, info=0)
            assert_equal(self.top_log.level, expect)
            assert_equal(self.console_handler.level, expect)
            assert_equal(self.file_handler.level, logging.CRITICAL)

            self.helper_log(particle, long_form, 'c', 'con',
                            expect, expect, logging.CRITICAL)
            self.helper_log(particle, long_form, 'c', 'console',
                            expect, expect, logging.CRITICAL)
            self.helper_log(particle, long_form, 'f', 'file',
                            expect, logging.CRITICAL, expect)

        herehere('d', 'debug', logging.DEBUG)
        herehere('i', 'info', logging.INFO)
        herehere('w', 'warning', logging.WARNING)
        herehere('e', 'error', logging.ERROR)
        herehere('c', 'critical', logging.CRITICAL)

        herehere(15)
        herehere(25)
        herehere(45)

        self.clear_log_state(logging.DEBUG)
        self.testee.commandme("set loglevel error")
        self.testee.assert_msg(errors=0, warnings=0, info=0)
        assert_equal(self.top_log.level, logging.DEBUG)
        assert_equal(self.console_handler.level, logging.ERROR)
        assert_equal(self.file_handler.level, logging.DEBUG)

    def test_log_level_negative(self):
        self.clear_log_state()
        self.testee.commandme("set loglevel unknown")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.assert_has_error('Invalid level')
        self.clear_log_state()
        self.testee.commandme("set loglevel d something")
        self.testee.assert_msg(errors=1, warnings=0, info=0)
        self.testee.assert_has_error('Invalid target argument')

        self.clear_log_state()
        self.testee.commandme("set loglevel x y z")
        self.testee.assert_has_error('Invalid list of arguments')

        self.clear_log_state()
        self.testee.commandme("set loglevel x y z t")
        self.testee.assert_has_error('Invalid list of arguments')


if __name__ == '__main__':
    import nose
    nose.runmodule()
