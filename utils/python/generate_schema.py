import os
import argparse  # Импортируем argparse, если еще не импортирован
from env_utils import EnvVarsUtils
from fs_utils import FsUtils
import re

def generate_markdown_schema(work_dir, schemas_dir):
    """Генерирует Markdown схему структуры папок, сохраняя секцию [#links to programms]."""
    markdown_content = ""
    programms_links_content = "\n[#links to programms\n" # Начальное значение секции links (плейсхолдер)

    md_schema_path = os.path.join(schemas_dir, "workspace_schema.md") # Путь к Markdown схеме
    existing_links_content = None # Переменная для хранения существующей секции links

    if os.path.exists(md_schema_path): # *** ПРОВЕРКА СУЩЕСТВОВАНИЯ ФАЙЛА СХЕМЫ ***
        try:
            with open(md_schema_path, "r", encoding="utf-8") as md_file:
                existing_markdown_content = md_file.read()
                links_section_match = re.search(r'\[#links to programms\n(.*?)\n\]', existing_markdown_content, re.DOTALL) # Ищем секцию links в существующем файле
                if links_section_match:
                    existing_links_content = links_section_match.group(1).strip() # Извлекаем содержимое существующей секции links
        except Exception as e:
            print(f"Ошибка при чтении существующего файла схемы: {e}") # Сообщение об ошибке чтения файла


    if existing_links_content: # *** ИСПОЛЬЗУЕМ СУЩЕСТВУЮЩУЮ СЕКЦИЮ LINKS, ЕСЛИ ОНА ЕСТЬ ***
        programms_links_content = f"\n[#links to programms\n{existing_links_content}\n]\n" # Используем существующее содержимое
        print("Используется существующая секция '[#links to programms]' из файла схемы.") # Информационное сообщение
    else: # *** ГЕНЕРИРУЕМ СЕКЦИЮ LINKS С ПЛЕЙСХОЛДЕРАМИ, ЕСЛИ СУЩЕСТВУЮЩЕЙ НЕТ ***
        programms_dir_path = os.path.join(work_dir, 'programms') # Путь к папке programms
        if os.path.isdir(programms_dir_path): # Проверяем, существует ли папка programms
            programms_subfolders = [
                d for d in os.listdir(programms_dir_path)
                if os.path.isdir(os.path.join(programms_dir_path, d)) and not d.startswith('.') # Получаем подпапки в programms, исключая dot-папки
            ]
            for subfolder_name in programms_subfolders:
                subfolder_path = os.path.join(programms_dir_path, subfolder_name)
                if any(os.path.isfile(os.path.join(subfolder_path, f)) for f in os.listdir(subfolder_path) if not f.startswith('.')): # Проверяем, есть ли файлы (не dot-файлы) в подпапке
                    programms_links_content += f"{subfolder_name} #link to $link_placeholder\n" # Добавляем placeholder link

        programms_links_content += "]\n" # Завершаем секцию links


    for root, dirs, files in os.walk(work_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]  # Игнорируем папки, начинающиеся с точки
        depth = root[len(work_dir) + len(os.sep):].count(os.sep)
        indent = '    ' * depth
        folder_name = os.path.basename(root)

        if folder_name == 'programms': # ***  ОБРАБОТКА ПАПКИ PROGRAMMS  ***
            dirs[:] = [] # ***  ОСТАНАВЛИВАЕМ OS.WALK ДЛЯ ПОДПАПОК PROGRAMMS  ***
            markdown_content += f"{indent}{folder_name}\n"
            markdown_content += f"{indent}    [comment: Содержит папки с исполняемыми файлами программ. Детализация - в разделе 'links to programms']\n" # Добавляем комментарий для папки programms
            continue # ***  ПЕРЕХОДИМ К СЛЕДУЮЩЕЙ ИТЕРАЦИИ OS.WALK  ***
        elif folder_name == '__pycache__' and 'utils' in root.split(os.sep) and 'python' in root.split(os.sep):
            dirs[:] = [] # Исключаем __pycache__ папки из utils/python
            continue # Пропускаем __pycache__ папки

        markdown_content += f"{indent}{folder_name}\n"

        for file in files:
            if file.endswith(('.py', '.json', '.md')): # *** ФИЛЬТРАЦИЯ ТИПОВ ФАЙЛОВ ***
                if root == os.path.join(work_dir, 'utils', 'python') and file == '__init__.py': # *** ИСКЛЮЧЕНИЕ __init__.py В utils/python ***
                    continue # Пропускаем __init__.py в utils/python

                file_base_name, file_extension = os.path.splitext(file) # Разделяем имя файла и расширение

                markdown_content += f"{indent}    {file} #.{file_extension[1:]} file\n" # Полное имя файла + тип
                markdown_content += f"{indent}        {file_base_name}\n" # Базовое имя файла


    markdown_content += programms_links_content # Добавляем сгенерированный content links в markdown

    return markdown_content


def get_utils_py_list(work_dir):
    """Генерирует список utils_py."""
    utils_py_list = []
    for root, dirs, files in os.walk(work_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]  # Игнорируем папки, начинающиеся с точки
        for file in files:
            if root == os.path.join(work_dir, 'utils', 'python') and file.endswith('.py'):
                file_name = os.path.basename(file)
                utils_py_list.append(file_name[:-3])
    return utils_py_list


def check_dangling_programms_links(work_dir, md_schema_content): # Новая функция для проверки "висящих" ссылок
    """Проверяет и возвращает список 'висящих' ссылок в папке programms, отсутствующих в Markdown схеме."""
    dangling_links = []
    programms_dir_path = os.path.join(work_dir, 'programms')
    if os.path.isdir(programms_dir_path):
        programms_subfolders = [d for d in os.listdir(programms_dir_path) if os.path.isdir(os.path.join(programms_dir_path, d)) and not d.startswith('.')]
        schema_links = []
        import re # Импортируем модуль re для регулярных выражений
        links_section_match = re.search(r'\[#links to programms\n(.*?)\n\]', md_schema_content, re.DOTALL) # Ищем секцию links в markdown
        if links_section_match:
            links_section = links_section_match.group(1) # Получаем содержимое секции links
            schema_links = [line.split('#')[0].strip() for line in links_section.strip().splitlines()] # Извлекаем имена ссылок из схемы

        for subfolder_name in programms_subfolders:
            if subfolder_name not in schema_links: # Проверяем, есть ли подпапка в схеме
                dangling_links.append(subfolder_name) # Если нет в схеме - это "висящая" ссылка

    return dangling_links


if __name__ == "__main__":
    print("--- Проверка переменных среды ---") # ***  НАЧАЛО ПРОВЕРКИ ПЕРЕМЕННЫХ СРЕДЫ  ***
    # Используем EnvVarsUtils для проверки переменных среды
    required_vars = ['$workdir']  # Список проверяемых переменных сред
    env_vars_ok = EnvVarsUtils.check_environment_variables(required_vars)

    if env_vars_ok:
        print("**Все необходимые переменные среды найдены.**") # ***  УСПЕШНАЯ ПРОВЕРКА ПЕРЕМЕННЫХ СРЕДЫ  ***
        work_dir_env = os.environ.get('$workdir') # Извлекаем переменную среды один раз
        work_dir = work_dir_env # Используем work_dir_env для work_dir
        schemas_dir = os.path.join(work_dir, 'schemas')
        md_schema_path = os.path.join(schemas_dir, "workspace_schema.md") # Путь к Markdown схеме
        print("--- Проверка папок ---") # ***  НАЧАЛО ПРОВЕРКИ ПАПОК  ***
        # Используем FsUtils для проверки папок
        required_folders = [schemas_dir] # Список проверяемых папок
        folders_ok = FsUtils.check_folders_exist_and_create(required_folders)

        if folders_ok:
          print("\n**Проверка папок завершена.**") # ***  УСПЕШНАЯ ПРОВЕРКА ПАПОК  ***
        else:
            print("\n**ВНИМАНИЕ: Проблемы с папками.**") # ***  ПРЕДУПРЕЖДЕНИЕ О ПРОБЛЕМАХ С ПАПКАМИ  ***
    else:
        print("\n**ВНИМАНИЕ: Проблемы с переменными среды.**") # ***  ПРЕДУПРЕЖДЕНИЕ О ПРОБЛЕМАХ С ПЕРЕМЕННЫМИ СРЕДЫ  ***

    # Продолжаем выполнение скрипта, только если основные проверки пройдены
    if work_dir and env_vars_ok and folders_ok: # Проверяем work_dir, env_vars_ok и folders_ok
        md_schema_content = generate_markdown_schema(work_dir, schemas_dir)
        utils_py_list = get_utils_py_list(work_dir)
        md_schema_path = os.path.join(schemas_dir, "workspace_schema.md")
        os.makedirs(schemas_dir, exist_ok=True) # redundant, но не страшно, exist_ok=True
        with open(md_schema_path, "w", encoding="utf-8") as md_file:
            md_file.write(md_schema_content)

        FsUtils.create_programms_symlinks(work_dir, md_schema_path) # ***  СОЗДАНИЕ СИМВОЛИЧЕСКИХ ССЫЛОК  ***

        dangling_links = FsUtils.check_dangling_symlinks_programms(work_dir, md_schema_content) # Проверяем "висящие" ссылки
        if dangling_links: # Если есть "висящие" ссылки
            print("\n**ВНИМАНИЕ: Обнаружены 'висящие' ссылки в папке programms:**") # ***  ПРЕДУПРЕЖДЕНИЕ О "ВИСЯЩИХ" ССЫЛКАХ  ***
            for link_info in dangling_links: # Выводим информацию о "висящих" симлинках
                folder_name = link_info['folder']
                symlinks = link_info['symlinks']
                print(f"  - В папке '{folder_name}':")
                for symlink in symlinks:
                    print(f"    - '{symlink}'")
            print("Пожалуйста, проверьте и удалите лишние симлинки вручную в папке 'programms'.") # Инструкция пользователю
        else:
            print("\n**Проверка 'висящих' ссылок в programms завершена. Висящих ссылок не обнаружено.**") # ***  СООБЩЕНИЕ ОБ ОТСУТСТВИИ "ВИСЯЩИХ" ССЫЛОК  ***


        print(f"Markdown схема создана и сохранена в {md_schema_path}") # ***  СООБЩЕНИЕ ОБ УСПЕШНОМ СОЗДАНИИ MARKDOWN СХЕМЫ  ***
        print(f"Список utils_py: {utils_py_list}")
        print("\n**Скрипт выполнен успешно.**") # ***  СООБЩЕНИЕ ОБ УСПЕШНОМ ВЫПОЛНЕНИИ СКРИПТА  ***


    else:
        print("\n**ВНИМАНИЕ: Скрипт не может быть выполнен из-за ошибок, указанных выше.**") # ***  ОБЩЕЕ ПРЕДУПРЕЖДЕНИЕ О НЕУДАЧЕ  ***
        print("Пожалуйста, устраните указанные выше проблемы и запустите скрипт снова.")