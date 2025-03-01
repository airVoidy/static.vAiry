import os

class FileUtils:
    """Утилиты для работы с файлами."""

    @staticmethod
    def find_and_replace_in_file(file_path, target_string, replacement_string, verbose=False):
        """Находит и заменяет target_string на replacement_string в файле.

        Args:
            file_path (str): Путь к файлу.
            target_string (str): Строка для поиска.
            replacement_string (str): Строка для замены.
            verbose (bool, optional): Выводить ли измененные строки. Defaults to False.

        Returns:
            list or None: Список измененных строк, если verbose=True, иначе None.
        """
        modified_lines = []
        file_changed = False
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            updated_lines = []
            for line in lines:
                if target_string in line:
                    modified_lines.append(line.strip())  # Сохраняем исходную строку для verbose
                    updated_line = line.replace(target_string, replacement_string)
                    updated_lines.append(updated_line)
                    file_changed = True  # Отмечаем, что файл был изменен
                else:
                    updated_lines.append(line)

            if file_changed:  # Записываем только если были изменения
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(updated_lines)

            if verbose and modified_lines:
                print(f"Замены произведены в файле: {file_path}")
                for original_line in modified_lines:
                    print(f"  Строка: '{original_line}'")
                return modified_lines
            else:
                return None

        except FileNotFoundError:
            print(f"Ошибка: Файл не найден: {file_path}")
            return None
        except Exception as e:
            print(f"Произошла ошибка при обработке файла: {file_path}")
            print(e)
            return None


    @staticmethod
    def find_lines_containing_substring(file_path, substring, verbose=False):
        """Находит строки в файле, содержащие заданную подстроку.

        Args:
            file_path (str): Путь к файлу.
            substring (str): Подстрока для поиска.
            verbose (bool, optional): Выводить ли найденные строки в консоль. Defaults to False.

        Returns:
            list: Список строк, содержащих подстроку.
        """
        found_lines = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if substring in line:
                        found_lines.append(line.strip())
                        if verbose:
                            print(line.strip())  # Выводим строку в консоль, если verbose=True
                return found_lines

        except FileNotFoundError:
            print(f"Ошибка: Файл не найден: {file_path}")
            return []  # Возвращаем пустой список, если файл не найден
        except Exception as e:
            print(f"Произошла ошибка при чтении файла: {file_path}")
            print(e)
            return []

    def find_and_replace_non_printable_chars_in_file(self, file_path, replacement_char=' '):
        """
        Находит и заменяет непечатаемые символы в файле.

        Args:
            file_path (str): Путь к файлу, в котором нужно произвести замену.
            replacement_char (str, optional): Символ для замены непечатаемых символов.
            По умолчанию - обычный пробел ' '.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
        except Exception as e:
            print(f"Ошибка при чтении файла: {file_path}")
            print(e)
            return False

        cleaned_content = ''
        replaced_count = 0
        for char in file_content:
            if ord(char) < 32 and char not in ('\n', '\r', '\t'):  # ASCII control characters excluding \n, \r, \t
                cleaned_content += replacement_char
                replaced_count += 1
            elif ord(char) == 160:  # Non-breaking space (U+00A0)
                cleaned_content += replacement_char
                replaced_count += 1
            else:
                cleaned_content += char

        if replaced_count > 0:
            print(f"Найдено и заменено {replaced_count} непечатаемых символов в файле: {file_path}")
        else:
            print(f"Непечатаемые символы не найдены в файле: {file_path}")

        try:
            with open(file_path, 'w', encoding='utf-8', newline='\n') as file:  # Ensure consistent line endings
                file.write(cleaned_content)
            return True
        except Exception as e:
            print(f"Ошибка при записи в файл: {file_path}")
            print(e)
            return False
    def fix_indentation_to_tabs(self, file_path, tab_width=4):
        """
        Преобразует отступы в файле в табуляцию, предполагая, что отступы сделаны пробелами.

        Args:
            file_path (str): Путь к файлу для обработки.
            tab_width (int, optional): Количество пробелов, которое считается одним уровнем отступа.
                                        По умолчанию - 4.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except Exception as e:
            print(f"Ошибка при чтении файла: {file_path}")
            print(e)
            return False

        updated_lines = []
        file_changed = False
        for line in lines:
            leading_spaces = 0
            for char in line:
                if char == ' ':
                    leading_spaces += 1
                else:
                    break

            if leading_spaces > 0:
                file_changed = True
                indentation_level = leading_spaces // tab_width # Определяем уровень отступа в табуляциях
                remaining_spaces = leading_spaces % tab_width # Остаток пробелов, если отступ не кратен tab_width

                new_line_indent = '\t' * indentation_level + ' ' * remaining_spaces + line[leading_spaces:] # Табуляция + остаток пробелами
                updated_lines.append(new_line_indent)
            else:
                updated_lines.append(line) # Строки без отступов оставляем как есть


        if file_changed:
            try:
                with open(file_path, 'w', encoding='utf-8', newline='\n') as file:
                    file.writelines(updated_lines)
                print(f"Табуляция в файле {file_path} успешно исправлена (заменена на табуляцию).")
                return True
            except Exception as e:
                print(f"Ошибка при записи в файл: {file_path}")
                print(e)
                return False
        else:
            print(f"Отступы в файле {file_path} уже соответствуют табуляции или отсутствуют пробельные отступы.")
            return True
if __name__ == '__main__':
    file_utils = FileUtils()

    # Пример использования find_and_replace_in_file
    test_file_path = 'test_file.txt'  # Создадим временный тестовый файл
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write("Это строка с target_string.\n")
        f.write("Другая строка без изменений.\n")
        f.write("Еще одна строка с target_string target_string again.\n")

    print(f"\n--- Пример find_and_replace_in_file ---")
    replaced_lines = file_utils.find_and_replace_in_file(
        test_file_path,
        target_string='target_string',
        replacement_string='replacement_string',
        verbose=True
    )
    if replaced_lines:
        print("\nИзмененные строки:")
        for line in replaced_lines:
            print(f"  '{line}'")

    print(f"\nСодержимое файла после замены:")
    with open(test_file_path, 'r', encoding='utf-8') as f:
        print(f.read())

    os.remove(test_file_path)  # Удаляем временный тестовый файл


    # Пример использования find_lines_containing_substring
    print(f"\n--- Пример find_lines_containing_substring ---")
    found_lines = file_utils.find_lines_containing_substring(
        'utils/python/generate_schema.py',  # Ищем в существующем файле
        substring='def ',
        verbose=True
    )
    if found_lines:
        print(f"\nСтроки, содержащие 'def ':")
        for line in found_lines:
            print(f"  '{line}'")