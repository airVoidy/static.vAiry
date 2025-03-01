import os

class EnvVarsUtils:
    """Утилиты для работы с переменными среды."""

    @staticmethod
    def get_env_var(var_name):
        """Получает значение переменной среды."""
        return os.environ.get(var_name)

    @staticmethod
    def set_env_var(var_name, var_value):
        """Устанавливает переменную среды (осторожно!)."""
        os.environ[var_name] = var_value

    @staticmethod
    def add_path_to_env_var(path_to_add, var_name='PATH'):
        """Добавляет путь к переменной среды PATH."""
        current_path = os.environ.get(var_name, '')
        separator = ';' if os.name == 'nt' else ':'
        if path_to_add not in current_path.split(separator):
            os.environ[var_name] = current_path + separator + path_to_add

    @staticmethod
    def get_dollar_vars():
        """Возвращает словарь переменных среды, начинающихся с $."""
        dollar_vars = {}
        for var_name, var_value in os.environ.items():
            if var_name.startswith('$'):
                dollar_vars[var_name] = var_value
        return dollar_vars

    @staticmethod
    def check_environment_variables(var_names):
        """Проверяет наличие переменных среды и выводит отчет."""
        missing_vars = []
        print("--- Проверка переменных среды ---")
        for var_name in var_names:
            var_value = EnvVarsUtils.get_env_var(var_name)
            if var_value:
                print(f"Переменная среды '{var_name}': найдена, значение = '{var_value}'")
            else:
                print(f"Переменная среды '{var_name}': **НЕ НАЙДЕНА**")
                missing_vars.append(var_name)

        if missing_vars:
            print("\n**ВНИМАНИЕ: Отсутствуют следующие переменные среды:**")
            for var_name in missing_vars:
                print(f"  - '{var_name}'")
            print("Пожалуйста, убедитесь, что эти переменные среды заданы.")
            return False  # Возвращает False, если есть отсутствующие переменные
        else:
            print("\n**Все необходимые переменные среды найдены.**")
            return True   # Возвращает True, если все переменные есть

# Пример использования (можно добавить в __main__ блок для тестирования)
if __name__ == '__main__':
    utils = EnvVarsUtils()
    # Пример проверки переменных среды
    required_vars = ['$workdir', '$utils_py']  # Список переменных для проверки
    vars_are_present = utils.check_environment_variables(required_vars)
    print(f"\nРезультат проверки переменных среды: {'Успешно' if vars_are_present else 'Неудача'}")

    if vars_are_present:
        workdir = utils.get_env_var('$workdir')
        print(f"Значение $workdir: {workdir}")
    else:
        print("Дальнейшие действия невозможны из-за отсутствия переменных среды.")