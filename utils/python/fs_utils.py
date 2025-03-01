import os

class FsUtils:
    """Утилиты для работы с файловой системой."""

    @staticmethod
    def check_folders_exist_and_create(folder_paths):
        """Проверяет существование папок и предлагает создать отсутствующие."""
        created_folders = []
        missing_folders = []
        existing_folders = []

        print("--- Проверка папок ---")
        for folder_path in folder_paths:
            if not os.path.exists(folder_path):
                print(f"Папка '{folder_path}': **НЕ СУЩЕСТВУЕТ**")
                missing_folders.append(folder_path)
            elif not os.path.isdir(folder_path):
                print(f"Путь '{folder_path}': существует, но **НЕ ЯВЛЯЕТСЯ ПАПКОЙ**") # Обработка случая, если путь - файл
                missing_folders.append(folder_path) # Считаем отсутствующей, так как нужна папка
            else:
                print(f"Папка '{folder_path}': найдена")
                existing_folders.append(folder_path)

        if missing_folders:
            print("\n**ВНИМАНИЕ: Отсутствуют следующие папки:**")
            for folder_path in missing_folders:
                create_choice = input(f"Создать папку '{folder_path}'? (y/n): ").lower()
                if create_choice == 'y':
                    try:
                        os.makedirs(folder_path, exist_ok=True) # Создаем папку и все родительские, если нужно
                        print(f"Папка '{folder_path}' успешно создана.")
                        created_folders.append(folder_path)
                    except OSError as e:
                        print(f"**Ошибка при создании папки '{folder_path}': {e}**")
                        return False # Возвращаем False, если не удалось создать критичную папку
                else:
                    print(f"Создание папки '{folder_path}' отменено пользователем.")
                    return False # Возвращаем False, если пользователь отказался создать критичную папку

        if created_folders:
            print("\n**Созданы следующие папки:**")
            for folder_path in created_folders:
                print(f"  - '{folder_path}'")

        if existing_folders:
            print("\n**Следующие папки уже существовали:**")
            for folder_path in existing_folders:
                print(f"  - '{folder_path}'")

        if missing_folders and not created_folders:
            print("\n**ВНИМАНИЕ: Необходимые папки отсутствуют и не были созданы.  Работа скрипта может быть нарушена.**")
            return False # Возвращаем False, если есть отсутствующие папки и не созданы
        else:
            print("\n**Проверка папок завершена.**")
            return True # Возвращаем True, если все необходимые папки есть (созданы или существовали)


if __name__ == '__main__':
    fs_utils = FsUtils()
    # Пример проверки и создания папок
    required_folders = ['schemas', 'non_existent_folder'] #  'schemas' должна существовать, 'non_existent_folder' - нет
    folders_ok = fs_utils.check_folders_exist_and_create(required_folders)
    print(f"\nРезультат проверки папок: {'Успешно' if folders_ok else 'Неудача'}")