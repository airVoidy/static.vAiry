import json
import os
from utils.python.generate_schema import get_utils_py_list # Импортируем get_utils_py_list

def convert_markdown_to_json(md_file_path, utils_py_list): # utils_py_list теперь передается как аргумент
    """Конвертирует Markdown схему в JSON, включая utils_py_list."""
    json_schema = {"name": "WORK", "type": "folder", "children": [], "utils_py": utils_py_list}
    current_level_folders = [json_schema["children"]]
    base_dir = os.path.dirname(md_file_path)

    with open(md_file_path, "r", encoding="utf-8") as md_file:
        for line in md_file:
            line = line.rstrip()
            if not line or line.startswith("[#links"):
                continue

            indent_level = line.count('    ')
            name_line = line.strip()

            if indent_level > 0 and name_line.startswith('- '):
                name_line = name_line[2:]
                name = name_line

            elif indent_level > 0 and name_line.startswith('>'):
                continue

            else:
                name = name_line

            item_path = os.path.join(base_dir, name)

            if os.path.isdir(item_path):
                item_type = "folder"
            elif os.path.isfile(item_path):
                item_type = "file"
            else:
                item_type = "file"

            new_item = {"name": name, "type": item_type, "children": []}

            if "[comment:" in name_line:
                comment_start = name_line.find("[comment:") + len("[comment:")
                comment_end = name_line.find("]", comment_start)
                if comment_end != -1:
                    new_item["comment"] = name_line[comment_start:comment_end].strip()
            if "[link:" in name_line:
                link_start = name_line.find("[link:") + len("[link:")
                link_end = name_line.find("]", link_start)
                if link_end != -1:
                    new_item["link"] = name_line[link_start:link_end].strip()


            if item_type == "folder":
                if indent_level > len(current_level_folders) -1 :
                    current_level_folders.append(current_level_folders[-1][-1]['children'])
                elif indent_level < len(current_level_folders) - 1:
                    current_level_folders = current_level_folders[:indent_level+1]

                current_level_folders[-1].append(new_item)
                current_level_folders.append(new_item['children'])
            elif item_type == "file":
                current_level_folders[-1].append(new_item)

    return json_schema


if __name__ == "__main__":
    work_dir = os.environ.get('workdir')
    schemas_dir = os.path.join(work_dir, 'schemas')
    md_schema_file = os.path.join(schemas_dir, "workspace_schema.md")
    if work_dir:
        utils_py_list = get_utils_py_list(work_dir) # Получаем utils_py_list ОТДЕЛЬНО
        json_schema = convert_markdown_to_json(md_schema_file, utils_py_list) # Передаем utils_py_list в конвертер
        json_schema_path = os.path.join(schemas_dir, "workspace_schema.json")
        os.makedirs(schemas_dir, exist_ok=True) # Redundant, but harmless
        with open(json_schema_path, "w", encoding="utf-8") as json_file:
            json.dump(json_schema, json_file, indent=4, ensure_ascii=False)

        print(f"JSON схема создана и сохранена в {json_schema_path}")
    else:
        print("Переменная среды workdir не определена.")