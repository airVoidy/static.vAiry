import os
from utils.python.env_utils import EnvVarsUtils
from utils.python.fs_utils import FsUtils

def generate_markdown_schema(work_dir, schemas_dir):
    """Генерирует Markdown схему структуры папок."""
    markdown_content = ""
    for root, dirs, files in os.walk(work_dir):
        depth = root[len(work_dir) + len(os.sep):].count(os.sep)
        indent = '    ' * depth
        folder_name = os.path.basename(root)
        markdown_content += f"{indent}{folder_name}\n"

        if folder_name == 'python':
            markdown_content += f"{indent}    ->python.exe #is PATH call!\n"
            markdown_content += f"{indent}    [comment: Вызовы Python интерпретатора]\n"

        for file in files:
            markdown_content += f"{indent}    {file}\n"
            file_name = os.path.basename(file)
            if folder_name == 'nekoray' and file_name == 'nekobox.exe':
                markdown_content += f"{indent}        -> nekobox.exe #link in programs!\n"
                markdown_content += f"{indent}        [link: $workdir call programm.nekobox]\n"
                markdown_content += f"{indent}        [comment: Исполняемый файл Nekobox VPN клиента]\n"

    markdown_content += "\n[#links to programms\n"
    markdown_content += "nekobox #link to nekobox.exe]\n"

    return markdown_content


def get_utils_py_list(work_dir):
    """Генерирует список utils_py."""
    utils_py_list = []
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            if root == os.path.join(work_dir, 'utils', 'python') and file.endswith('.py'):
                file_name = os.path.basename(file)
                utils_py_list.append(file_name[:-3])
    return utils_py_list


if __name__ == "__main__":
    work_dir = os.environ.get('workdir')
    schemas_dir = os.path.join(work_dir, 'schemas')

    # Используем EnvVarsUtils для проверки переменных среды
    required_vars = ['workdir']  # Список проверяемых переменных сред
    env_vars_ok = EnvVarsUtils.check_environment_variables(required_vars)

    # Используем FsUtils для проверки папок
    required_folders = [schemas_dir] # Список проверяемых папок
    folders_ok = FsUtils.check_folders_exist_and_create(required_folders)

    # Продолжаем выполнение скрипта, только если все проверки пройдены
    if work_dir and env_vars_ok and folders_ok:
        md_schema_content = generate_markdown_schema(work_dir, schemas_dir)
        utils_py_list = get_utils_py_list(work_dir)
        md_schema_path = os.path.join(schemas_dir, "workspace_schema.md")
        os.makedirs(schemas_dir, exist_ok=True) # redundant, но не страшно, exist_ok=True
        with open(md_schema_path, "w", encoding="utf-8") as md_file:
            md_file.write(md_schema_content)
        print(f"Markdown схема создана и сохранена в {md_schema_path}")
        print(f"Список utils_py: {utils_py_list}")
    else:
        print("\n**ВНИМАНИЕ: Скрипт не может быть выполнен из-за ошибок в переменных среды или папках.**")
        print("Пожалуйста, устраните указанные выше проблемы и запустите скрипт снова.")