import unittest
import os
from env_utils import EnvVarsUtils

class TestEnvVarsUtils(unittest.TestCase): # Создаем тестовый класс, наследуясь от unittest.TestCase

    def test_get_env_var_existing(self): # Тест для существующей переменной среды
        os.environ['TEST_VAR_EXISTING'] = 'test_value' # Устанавливаем тестовую переменную среды
        value = EnvVarsUtils.get_env_var('TEST_VAR_EXISTING')
        self.assertEqual(value, 'test_value') # Проверяем, что полученное значение соответствует ожидаемому
        del os.environ['TEST_VAR_EXISTING'] # Удаляем тестовую переменную среды после теста

    def test_get_env_var_non_existing(self): # Тест для несуществующей переменной среды
        value = EnvVarsUtils.get_env_var('TEST_VAR_NON_EXISTING')
        self.assertIsNone(value) # Проверяем, что для несуществующей переменной возвращается None

    def test_check_environment_variables_all_exist(self): # Тест, когда все переменные среды существуют
        os.environ['TEST_VAR_1'] = 'value1'
        os.environ['TEST_VAR_2'] = 'value2'
        vars_to_check = ['TEST_VAR_1', 'TEST_VAR_2']
        result = EnvVarsUtils.check_environment_variables(vars_to_check)
        self.assertTrue(result) # Проверяем, что функция вернула True (все переменные найдены)
        del os.environ['TEST_VAR_1']
        del os.environ['TEST_VAR_2']

    def test_check_environment_variables_one_missing(self): # Тест, когда одна переменная среды отсутствует
        os.environ['TEST_VAR_3'] = 'value3'
        vars_to_check = ['TEST_VAR_3', 'TEST_VAR_MISSING']
        result = EnvVarsUtils.check_environment_variables(vars_to_check)
        self.assertFalse(result) # Проверяем, что функция вернула False (есть отсутствующие переменные)
        del os.environ['TEST_VAR_3']

    def test_get_dollar_vars(self): # Тест для get_dollar_vars
        os.environ['$DOLLAR_VAR_1'] = 'dollar_value1'
        os.environ['$DOLLAR_VAR_2'] = 'dollar_value2'
        os.environ['REGULAR_VAR'] = 'regular_value'
        dollar_vars = EnvVarsUtils.get_dollar_vars()
        self.assertIn('$DOLLAR_VAR_1', dollar_vars) # Проверяем, что $DOLLAR_VAR_1 есть в словаре
        self.assertIn('$DOLLAR_VAR_2', dollar_vars) # Проверяем, что $DOLLAR_VAR_2 есть в словаре
        self.assertNotIn('REGULAR_VAR', dollar_vars) # Проверяем, что REGULAR_VAR отсутствует в словаре
        self.assertEqual(dollar_vars['$DOLLAR_VAR_1'], 'dollar_value1') # Проверяем значение $DOLLAR_VAR_1
        self.assertEqual(dollar_vars['$DOLLAR_VAR_2'], 'dollar_value2') # Проверяем значение $DOLLAR_VAR_2
        del os.environ['$DOLLAR_VAR_1']
        del os.environ['$DOLLAR_VAR_2']
        del os.environ['REGULAR_VAR']

if __name__ == '__main__':
    unittest.main() # Запуск тестов, если файл запущен напрямую