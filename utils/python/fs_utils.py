import os
import re

class FsUtils:
    """Утилиты для работы с файловой системой."""

    @staticmethod
    def check_folders_exist_and_create(folders):
        """Проверяет существование папок и создает отсутствующие."""
        folders_ok = True
        created_folders = []
        existing_folders = []

        print("--- Проверка папок ---") # ***  НАЧАЛО ПРОВЕРКИ ПАПОК  ***

        for folder in folders:
            if not os.path.exists(folder):
                try:
                    os.makedirs(folder, exist_ok=True)
                    created_folders.append(folder)
                    folders_ok = False # Помечаем как не OK, если были созданы папки
                except OSError as e:
                    print(f"Ошибка создания папки '{folder}': {e}")
                    folders_ok = False
            else:
                existing_folders.append(folder)

        if created_folders:
            print("\n**Были созданы следующие папки:**") # *** СООБЩЕНИЕ О СОЗДАННЫХ ПАПКАХ ***
            for folder in created_folders:
                print(f"  - '{folder}'")

        if existing_folders:
            print("\n**Следующие папки уже существовали:**") # *** СООБЩЕНИЕ О СУЩЕСТВУЮЩИХ ПАПКАХ ***
            for folder in existing_folders:
                print(f"  - '{folder}'")

        if folders_ok:
            print("\n**Все необходимые папки найдены.**") # *** СООБЩЕНИЕ ОБ УСПЕШНОЙ ПРОВЕРКЕ ПАПОК ***
        else:
            print("\n**ВНИМАНИЕ: Проблемы с папками.**") # *** ПРЕДУПРЕЖДЕНИЕ О ПРОБЛЕМАХ С ПАПКАМИ ***

        print("**Проверка папок завершена.**") # ***  ЗАВЕРШЕНИЕ ПРОВЕРКИ ПАПОК  ***
        return folders_ok


    @staticmethod
    def create_programms_symlinks(work_dir, md_schema_path):
        """Создает символические ссылки в папке programms на основе Markdown схемы,
        разделяя логику для файлов и путей.""" # *** ОБНОВЛЕННОЕ ОПИСАНИЕ ***
        programms_dir_path = os.path.join(work_dir, 'programms')
        md_schema_content = ""

        try:
            with open(md_schema_path, "r", encoding="utf-8") as md_file:
                md_schema_content = md_file.read()
        except FileNotFoundError:
            print(f"Ошибка: Файл Markdown схемы не найден по пути: {md_schema_path}")
            return

        links_section_match = re.search(r'\[#links to programms\n(.*?)\n\]', md_schema_content, re.DOTALL)
        if not links_section_match:
            print("Секция '[#links to programms]' не найдена в Markdown схеме.")
            return

        links_section = links_section_match.group(1)
        links_lines = links_section.strip().splitlines()

        print("\n--- Создание символических ссылок в programms ---") # *** НАЧАЛО СОЗДАНИЯ СИМВОЛИЧЕСКИХ ССЫЛОК ***
        
        for line in links_lines:
            parts = line.split('#link to')
            #print(f"parts: {parts}")
            link_targets = []
            if len(parts) >= 2:
                for part in enumerate(parts):  # part - это кортеж (индекс, значение)
                    #print(f"part[0]: {part[0]}")
                    #print(f"part[1]: {part[1]}")
                    if part[0] == 0:
                        subfolder_name = part[1].strip()  # Добавляем очистку от пробелов
                    else:
                        # Правильное использование append
                        link_targets.append(part[1].strip())  # Убираем пробелы вокруг названий
                    print(f"part: {part}")
                subfolder_programms_path = os.path.join(programms_dir_path, subfolder_name) # Путь к подпапке programms
                os.makedirs(subfolder_programms_path, exist_ok=True) # Создаем подпапку, если ее нет

                for link_target in link_targets:
                    print(f"link_target: {link_target}")
                    if not link_target: # Пропускаем пустые ссылки, если вдруг попадутся
                        continue

                    # ***  РАЗДЕЛЕНИЕ ЛОГИКИ ОБРАБОТКИ ПУТИ/ФАЙЛА  ***
                    if os.sep in link_target: # ***  ЕСЛИ link_target СОДЕРЖИТ РАЗДЕЛИТЕЛЬ ПУТИ (ПУТЬ) ***
                        target_path = os.path.normpath(os.path.join(subfolder_programms_path, link_target.replace('\\', '/').lstrip('/')))
                        print(f"target_path is {target_path}")
                    else: # ***  ИНАЧЕ (ПРОСТО ИМЯ ФАЙЛА) ***
                        found_target_path = None
                        for root, _, files in os.walk(work_dir): # Используем os.walk для поиска файла
                            for file in files:
                                if file == link_target: # Ищем файл по имени (базовому имени)
                                    found_target_path = os.path.join(root, file) # Нашли путь к файлу
                                    break # Выходим из внутреннего цикла (файлов)
                            if found_target_path: # Если файл найден, выходим и из внешнего цикла (папок)
                                break
                        target_path = found_target_path # Используем найденный путь (или None, если не найден)
                    # ***  КОНЕЦ РАЗДЕЛЕНИЯ ЛОГИКИ  ***


                    if target_path and os.path.exists(target_path): # *** ПРОВЕРКА target_path ПЕРЕД СОЗДАНИЕМ СИМЛИНКА ***
                        link_name = os.path.basename(link_target)
                        symlink_path = os.path.join(programms_dir_path, link_name)

                        if not os.path.exists(symlink_path): # Проверяем, существует ли уже симлинк
                            try:
                                os.symlink(target_path, symlink_path) # Создаем символическую ссылку
                                print(f"  Создана симлическая ссылка: '{symlink_path}' -> '{target_path}'") # СООБЩЕНИЕ О СОЗДАНИИ СИМЛИНКА
                            except OSError as e:
                                print(f"  Ошибка создания симлической ссылки '{symlink_path}' -> '{target_path}': {e}") # СООБЩЕНИЕ ОБ ОШИБКЕ СОЗДАНИЯ СИМЛИНКА
                        else:
                            print(f"  Симлическая ссылка уже существует: '{symlink_path}'") # СООБЩЕНИЕ О СУЩЕСТВОВАНИИ СИМЛИНКА
                    else: # ***  ОБЪЕДИНЕННОЕ СООБЩЕНИЕ О НЕ НАЙДЕННОМ ФАЙЛЕ (ДЛЯ ОБОИХ СЛУЧАЕВ) ***
                        print(f"  Файл не найден по пути или имени: '{link_target}' (ссылка для '{subfolder_name}')") # ПРЕДУПРЕЖДЕНИЕ О НЕ НАЙДЕННОМ ФАЙЛЕ

            elif parts[0].strip(): # Предупреждение, если строка не соответствует формату #link to, но не пустая
                print(f"  Предупреждение: Строка не соответствует формату '#link to' и будет проигнорирована: '{line.strip()}'")

        print("**Создание символических ссылок в programms завершено.**") # *** ЗАВЕРШЕНИЕ СОЗДАНИЯ СИМВОЛИЧЕСКИХ ССЫЛОК ***


    @staticmethod
    def check_dangling_symlinks_programms(work_dir, md_schema_content):
        """Проверяет и возвращает список 'висящих' симлинков в папке programms."""
        dangling_links = []
        programms_dir_path = os.path.join(work_dir, 'programms')
        if not os.path.isdir(programms_dir_path):
            return dangling_links # Если папки programms нет, то и висящих ссылок нет

        schema_links_subfolders = set() # Используем set для быстрого поиска подпапок из схемы
        import re # Импортируем модуль re для регулярных выражений
        links_section_match = re.search(r'\[#links to programms\n(.*?)\n\]', md_schema_content, re.DOTALL) # Ищем секцию links в markdown
        if links_section_match:
            links_section = links_section_match.group(1) # Получаем содержимое секции links
            schema_links_subfolders = set(line.split('#')[0].strip() for line in links_section.strip().splitlines()) # Извлекаем имена подпапок из схемы и добавляем в set

        programms_subfolders = [d for d in os.listdir(programms_dir_path) if os.path.isdir(os.path.join(programms_dir_path, d)) and not d.startswith('.')]

        for subfolder_name in programms_subfolders:
            if subfolder_name not in schema_links_subfolders: # Проверяем, есть ли подпапка в схеме
                subfolder_path = os.path.join(programms_dir_path, subfolder_name)
                symlinks_in_subfolder = [item for item in os.listdir(subfolder_path) if os.path.islink(os.path.join(subfolder_path, item))]
                if symlinks_in_subfolder: # Проверяем, есть ли симлинки в "висящей" подпапке
                    dangling_links.append({'folder': subfolder_name, 'symlinks': symlinks_in_subfolder}) # Добавляем информацию о "висящей" папке и ее симлинках

        return dangling_links

if __name__ == '__main__':
    fs_utils = FsUtils()
    # Пример проверки и создания папок
    required_folders = ['schemas', 'non_existent_folder'] #  'schemas' должна существовать, 'non_existent_folder' - нет
    folders_ok = fs_utils.check_folders_exist_and_create(required_folders)
    print(f"\nРезультат проверки папок: {'Успешно' if folders_ok else 'Неудача'}")