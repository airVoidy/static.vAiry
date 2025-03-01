import os
import subprocess

class CmdUtils:
    """Утилиты для запуска команд CMD через Python."""

    @staticmethod
    def run_cmd_command(command):
        """Запускает команду CMD и возвращает вывод."""
        try:
            process = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return process.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Ошибка выполнения команды: {command}")
            print(f"Код ошибки: {e.returncode}")
            print(f"Вывод ошибки:\n{e.stderr.strip()}")
            return None

    @staticmethod
    def run_and_print_cmd_command(command):
        """Запускает команду CMD и выводит результат в консоль в реальном времени."""
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            return_code = process.poll()
            if return_code != 0:
                error_output = process.stderr.read()
                print(f"Ошибка выполнения команды: {command}")
                print(f"Код ошибки: {return_code}")
                print(f"Вывод ошибки:\n{error_output.strip()}")
                return None
            return return_code
        except Exception as e:
            print(f"Общая ошибка при запуске команды: {command}")
            print(e)
            return None


if __name__ == '__main__':
    cmd_utils = CmdUtils()
    # Пример запуска простой команды и получения вывода
    output = cmd_utils.run_cmd_command("dir")
    if output:
        print("Вывод команды 'dir':")
        print(output)

    # Пример запуска команды с выводом в реальном времени
    print("\nВыполнение команды 'ipconfig /all' с выводом в реальном времени:")
    cmd_utils.run_and_print_cmd_command("ipconfig /all")