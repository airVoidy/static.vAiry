import json
import os
from generate_schema import get_utils_py_list # Импортируем get_utils_py_list

@staticmethod
def convert_markdown_to_json(md_file_path, utils_py_list): # Функция теперь принимает md_file_path и utils_py_list
    """Конвертирует Markdown схему в иерархический JSON, включая utils_py_list и секцию [#links to programms]."""
    json_schema = {"type":"json_schema","name":"workspace_schema","contents": [], "utils_py": utils_py_list, "indent_level": 0} # Корневой элемент JSON с indent_level = 0    programms_links = [] # Список для хранения programms_links
    programms_links = [] # Список для хранения programms_links

    folder_stack = [json_schema] # Стек для отслеживания текущей папки в иерархии
    base_dir = os.path.dirname(md_file_path)
    in_links_section = False # Флаг для секции links

    with open(md_file_path, "r", encoding="utf-8") as md_file:
        file_name_line_buffer = None # Буфер для полного имени файла

        for line in md_file:
            line = line.rstrip()
            if not line: # Пропускаем пустые строки
                continue
            if line.startswith("[#links to programms"): # Начало секции links
                in_links_section = True
                continue
            elif line.startswith("]"): # Конец секции links
                in_links_section = False
                continue

            if in_links_section: # Обработка строк секции links
                parts = line.strip().split('#link to')
                if len(parts) >= 2:
                    program_name = parts[0].strip()
                    link_targets = [lt.strip() for lt in parts[1:]]
                    programms_links.append({"name": program_name, "links": link_targets})
                continue # Переходим к следующей строке после обработки links

            indent_level = line.count('    ') # 4 пробела для отступа
            name_line = line.strip()

            # Обработка изменения уровня отступа для иерархии
            while indent_level < folder_stack[-1]["indent_level"]:
                folder_stack.pop() # Выход из папки, если отступ уменьшился

            item_data = {} # Данные для текущего элемента
            item_data["indent_level"] = indent_level # Сохраняем уровень отступа

            if indent_level > 0 and name_line.startswith('- '): # listItem
                item_data["type"] = "listItem"
                item_data["name"] = name_line[2:]
            elif indent_level > 0 and name_line.startswith('>'): # quote
                item_data["type"] = "quote"
                item_data["content"] = name_line[1:].strip()
            elif indent_level > 0 and "#." in name_line and name_line.endswith("file"): # file (с расширением)
                file_name_line_buffer = name_line # Буферизация полного имени файла
                continue # Ожидаем базовое имя файла на следующей строке
            elif file_name_line_buffer: # Обработка базового имени файла (следующая строка после полного имени)
                file_full_name_line = file_name_line_buffer
                file_base_name = name_line
                file_extension_start = file_full_name_line.find("#.") + 2 # Находим начало расширения (после "#.")
                file_extension_end = file_full_name_line.find(" ", file_extension_start)
                file_extension = file_full_name_line[file_extension_start:file_extension_end] if file_extension_end != -1 else file_full_name_line[file_extension_start:]
                item_data["type"] = "file"
                item_data["name"] = file_full_name_line.split(" #")[0] # Полное имя
                item_data["base_name"] = file_base_name # Базовое имя
                item_data["extension"] = file_extension # Расширение
                file_name_line_buffer = None # Очищаем буфер
            elif "[comment:" in name_line: # comment
                comment_start = name_line.find("[comment:") + len("[comment:")
                comment_end = name_line.find("]", comment_start)
                if comment_end != -1:
                    item_data["type"] = "comment"
                    item_data["content"] = name_line[comment_start:comment_end].strip()
            elif "[link:" in name_line: # link
                link_start = name_line.find("[link:") + len("[link:")
                link_end = name_line.find("]", link_start)
                if link_end != -1:
                    item_data["type"] = "link"
                    item_data["target"] = name_line[link_start:link_end].strip()
                    item_data["name"] = name_line.split(" [")[0].strip() # Имя ссылки до " ["
            else: # folder
                item_data["type"] = "folder"
                item_data["name"] = name_line
                item_data["contents"] = [] # Инициализируем список contents для папки
                folder_stack[-1]["contents"].append(item_data) # Добавляем как дочерний элемент к текущей папке
                folder_stack.append(item_data) # Делаем текущую папку - новой текущей папкой

            if item_data: # Добавляем item_data только если он не пустой (не пропущен continue)
                    if item_data.get("type") != "folder": # Для папок contents добавляются выше
                        folder_stack[-1]["contents"].append(item_data) # Добавляем элемент к contents текущей папки

        if programms_links: # Добавляем programms_links в JSON, если есть
            json_schema["programms_links"] = programms_links

        return json_schema


if __name__ == "__main__":
    work_dir_env = os.environ.get('workdir')
    work_dir = work_dir_env if work_dir_env else "."
    schemas_dir = os.path.join(work_dir, 'schemas')
    md_schema_path = os.path.join(schemas_dir, "workspace_schema.md")
    json_schema_path = os.path.join(schemas_dir, "workspace_schema.json")

    # ***  ВОССТАНОВЛЕННАЯ ЛОГИКА ДЛЯ utils_py_list (скопировано из generate_schema.py) ***
    utils_py_dir = os.path.join(work_dir, 'utils', 'python') # Путь к папке utils/python
    utils_py_list = [filename[:-3] for filename in os.listdir(utils_py_dir) if filename.endswith(".py") and filename != "__init__.py"] # Получаем список .py файлов
    # ***  КОНЕЦ ВОССТАНОВЛЕНИЯ ЛОГИКИ utils_py_list ***


    try:
        # Теперь вызываем функцию ConvertMdToJson.convert_markdown_to_json правильно
        json_output = convert_markdown_to_json(md_schema_path, utils_py_list)
    except FileNotFoundError:
        print(f"Ошибка: Файл Markdown схемы не найден: {md_schema_path}")
        exit(1)


    with open(json_schema_path, "w", encoding="utf-8") as json_file:
        json.dump(json_output, json_file, indent=4, ensure_ascii=False)

    print(f"Иерархическая JSON схема успешно создана и сохранена в: {json_schema_path}")