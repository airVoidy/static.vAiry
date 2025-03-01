import unittest
import os
import tempfile
import builtins  # Импортируем модуль builtins
from fs_utils import FsUtils

class TestFsUtils(unittest.TestCase):


	def test_check_folders_exist_and_create_existing_folder(self):
		with tempfile.TemporaryDirectory() as temp_dir: # Создаем временную директорию
			test_folder_path = os.path.join(temp_dir, 'test_folder')
			os.makedirs(test_folder_path) # Создаем тестовую папку внутри временной

			folders_to_check = [test_folder_path]
			result = FsUtils.check_folders_exist_and_create(folders_to_check)
			self.assertTrue(result) # Проверяем, что для существующей папки возвращается True

	def test_check_folders_exist_and_create_non_existing_folder_create_yes(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			test_folder_path = os.path.join(temp_dir, 'non_existent_folder')

		def mock_input(prompt):
			return 'y'
            
		# Сохраняем и подменяем input через модуль builtins
		original_input = builtins.input
		builtins.input = mock_input

		folders_to_check = [test_folder_path]
		result = FsUtils.check_folders_exist_and_create(folders_to_check)
		self.assertTrue(result)
		self.assertTrue(os.path.exists(test_folder_path))

		builtins.input = original_input  # Восстанавливаем

	def test_check_folders_exist_and_create_non_existing_folder_create_no(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			test_folder_path = os.path.join(temp_dir, 'non_existent_folder')

		def mock_input(prompt):
			return 'n'
            
		# Аналогично исправляем здесь
		original_input = builtins.input
		builtins.input = mock_input

		folders_to_check = [test_folder_path]
		result = FsUtils.check_folders_exist_and_create(folders_to_check)
		self.assertFalse(result)
		self.assertFalse(os.path.exists(test_folder_path))

		builtins.input = original_input

	# Добавьте другие тесты для FsUtils (например, для случая, когда путь - файл, а не папка)


if __name__ == '__main__':
	unittest.main()