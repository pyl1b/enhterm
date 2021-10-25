import os
from unittest import TestCase
from unittest.mock import MagicMock

from enhterm.variables import VariablesMixin, add_cd_variable, add_cdn_variable


class TestFunctions(TestCase):
    def test_add_cd_variable(self):
        testee = VariablesMixin()
        add_cd_variable(testee)
        self.assertTrue(os.path.isdir(testee['cd']))
        self.assertEquals(len(testee), 1)

    def add_cdn_variable(self):
        testee = VariablesMixin()
        add_cdn_variable(testee)
        result = testee['cdn']
        self.assertEqual(os.path.basename(os.getcwd()), result)
        self.assertEquals(len(testee), 1)


class TestVariablesMixin(TestCase):
    def setUp(self):
        self.testee = VariablesMixin(
            variables={
                'ABC': MagicMock(return_value='123'),
                'DEF': MagicMock(return_value='456'),
            }
        )

    def tearDown(self):
        self.testee = None

    def test_init(self):
        testee = VariablesMixin()
        self.assertDictEqual(testee.variables, {})

        par_in = MagicMock()
        testee = VariablesMixin(variables=par_in)
        self.assertEquals(testee.variables, par_in)

    def test_variable_value_exists(self):
        exc = MagicMock(spec=Exception)
        self.assertEquals(
            self.testee.variable_value('ABC', default='1001', raise_if_missing=exc),
            "123"
        )
        self.testee.variables['ABC'].assert_called_once()
        self.testee.variables['DEF'].assert_not_called()

    def test_variable_value_returns_default(self):
        self.assertEquals(
            self.testee.variable_value('XYZ', default='1001', raise_if_missing=None),
            "1001"
        )
        self.testee.variables['ABC'].assert_not_called()
        self.testee.variables['DEF'].assert_not_called()

    def test_variable_value_raises(self):
        with self.assertRaises(Exception):
            self.testee.variable_value('XYZ', default='1001', raise_if_missing=Exception)
        self.testee.variables['ABC'].assert_not_called()
        self.testee.variables['DEF'].assert_not_called()

    def test_add_variables(self):
        self.testee.add_variables({
            'GHI': MagicMock(return_value='444'),
            'JJJ': MagicMock(return_value='555'),
        })
        self.assertIn('ABC', self.testee.variables)
        self.assertIn('DEF', self.testee.variables)
        self.assertIn('GHI', self.testee.variables)
        self.assertIn('JJJ', self.testee.variables)
        self.assertEquals(len(self.testee.variables), 4)
        self.assertEquals(self.testee.variable_value('ABC'), "123")
        self.assertEquals(self.testee.variable_value('DEF'), "456")
        self.assertEquals(self.testee.variable_value('GHI'), "444")
        self.assertEquals(self.testee.variable_value('JJJ'), "555")

    def test_add_variable(self):
        self.testee.add_variable('GHI', MagicMock(return_value='444'))
        self.assertIn('ABC', self.testee.variables)
        self.assertIn('DEF', self.testee.variables)
        self.assertIn('GHI', self.testee.variables)
        self.assertEquals(len(self.testee.variables), 3)
        self.assertEquals(self.testee.variable_value('ABC'), "123")
        self.assertEquals(self.testee.variable_value('DEF'), "456")
        self.assertEquals(self.testee.variable_value('GHI'), "444")

    def test_rem_variable(self):
        self.testee.rem_variable('ABC')
        self.assertNotIn('ABC', self.testee.variables)
        self.assertIn('DEF', self.testee.variables)
        self.assertEquals(len(self.testee.variables), 1)
        self.assertEquals(self.testee.variable_value('DEF'), "456")

        with self.assertRaises(KeyError):
            self.testee.rem_variable('ABC')

    def test_values(self):
        self.assertDictEqual(
            self.testee.values(),
            {
                'ABC': "123",
                "DEF": "456"
            }
        )

    def test_clear_variables(self):
        self.testee.clear_variables()
        self.assertDictEqual(self.testee.variables, {})
        self.testee.clear_variables()
        self.assertDictEqual(self.testee.variables, {})

    def test_get(self):
        self.assertEquals(self.testee.get('ABC'), "123")
        self.assertEquals(self.testee.get('DEF'), "456")
        self.assertEquals(self.testee.get('ABC', default=100), "123")
        self.assertEquals(self.testee.get('DEF', default=1000), "456")
        self.assertEquals(self.testee.get('ABCX', default=100), 100)
        self.assertEquals(self.testee.get('DEFX', default=1000), 1000)

    def test_items_list(self):
        self.assertListEqual(self.testee.items_list(), [('ABC', '123'), ('DEF', '456')])

    def test_items(self):
        self.assertListEqual(self.testee.items_list(), [('ABC', '123'), ('DEF', '456')])

    def test_keys(self):
        self.assertListEqual(self.testee.keys(), ['ABC', 'DEF'])

    def test_contains(self):
        self.assertIn('ABC', self.testee)
        self.assertIn('DEF', self.testee)
        self.assertNotIn('ABCX', self.testee)
        self.assertNotIn('DEFX', self.testee)

    def test_del(self):
        del self.testee['ABC']
        with self.assertRaises(KeyError):
            del self.testee['ABC']

    def test_get_item(self):
        self.assertEquals(self.testee['ABC'], '123')
        self.assertEquals(self.testee['DEF'], '456')
        with self.assertRaises(KeyError):
            _ = self.testee['ABCX']

    def test_len(self):
        self.assertEquals(len(self.testee), 2)

    def test_replace_in_str(self):
        self.assertEquals(self.testee.replace_in_string('xxxxx'), 'xxxxx')
        self.assertEquals(self.testee.replace_in_string('xxx{ABC}xx'), 'xxx123xx')
        self.assertEquals(self.testee.replace_in_string('{ABC}xxxxx'), '123xxxxx')
        self.assertEquals(self.testee.replace_in_string('xxxxx{ABC}'), 'xxxxx123')
        self.assertEquals(self.testee.replace_in_string('{ABC}'), '123')

        self.assertEquals(self.testee.replace_in_string('xxx{DEF}xx'), 'xxx456xx')
        self.assertEquals(self.testee.replace_in_string('{DEF}xxxxx'), '456xxxxx')
        self.assertEquals(self.testee.replace_in_string('xxxxx{DEF}'), 'xxxxx456')
        self.assertEquals(self.testee.replace_in_string('{DEF}'), '456')

        self.assertEquals(self.testee.replace_in_string('{ABC}xxx{DEF}xx'), '123xxx456xx')
        self.assertEquals(self.testee.replace_in_string('{DEF}xxxxx{ABC}'), '456xxxxx123')
        self.assertEquals(self.testee.replace_in_string('xxxxx{DEF}{ABC}'), 'xxxxx456123')
        self.assertEquals(self.testee.replace_in_string('{ABC}{DEF}'), '123456')
        self.assertEquals(self.testee.replace_in_string('{ABC}{DEF}{ABC}{DEF}'), '123456123456')

        self.assertEquals(
            self.testee.replace_in_string('xxx{ABCX}xx', raise_if_missing=False),
            'xxxxx'
        )
        self.assertEquals(
            self.testee.replace_in_string('{DEFX}xxx{ABCX}xx', raise_if_missing=False),
            'xxxxx'
        )
        self.assertEquals(
            self.testee.replace_in_string('{DEFX}xxx{ABCX}xx{GTRE}', raise_if_missing=False),
            'xxxxx'
        )
        self.assertEquals(
            self.testee.replace_in_string('{ABC}xxx{ABCX}xx{DEF}', raise_if_missing=False),
            '123xxxxx456'
        )

        with self.assertRaises(KeyError):
            _ = self.testee.replace_in_string('xxx{ABCX}xx', raise_if_missing=True)
        with self.assertRaises(KeyError):
            _ = self.testee.replace_in_string('{DEFX}xxx{ABCX}xx', raise_if_missing=True)
        with self.assertRaises(KeyError):
            _ = self.testee.replace_in_string('{DEFX}xxx{ABCX}xx{GTRE}', raise_if_missing=True)
        with self.assertRaises(KeyError):
            _ = self.testee.replace_in_string('{ABC}xxx{ABCX}xx{DEF}', raise_if_missing=True)

