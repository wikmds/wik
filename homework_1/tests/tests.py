import unittest
import os
import tarfile
import json
from main import Emulator

class EmulatorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Этот метод будет выполнен один раз перед всеми тестами. Здесь мы создадим тестовый архив.
        """
        # Создаем временный TAR-архив для тестов
        cls.test_vfs_path = 'test_vfs.tar'
        with tarfile.open(cls.test_vfs_path, 'w') as tar:
            # Создаем директории и файлы внутри архива
            file1 = tarfile.TarInfo('dir1/file1.txt')
            file1.size = 0
            tar.addfile(file1)

            file2 = tarfile.TarInfo('dir1/file2.txt')
            file2.size = 0
            tar.addfile(file2)

            file3 = tarfile.TarInfo('dir2/file3.txt')
            file3.size = 0
            tar.addfile(file3)

    @classmethod
    def tearDownClass(cls):
        """
        Этот метод будет выполнен один раз после всех тестов. Здесь удаляем временный архив.
        """
        if os.path.exists(cls.test_vfs_path):
            os.remove(cls.test_vfs_path)

    def setUp(self):
        """
        Этот метод выполняется перед каждым тестом.
        Здесь мы инициализируем эмулятор с тестовым архивом.
        """
        config = {'vfs_path': self.test_vfs_path}
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file)

        self.emulator = Emulator('config.json')

    def tearDown(self):
        """
        Этот метод выполняется после каждого теста. Здесь очищаем ресурсы.
        """
        self.emulator.cleanup()

    def test_ls(self):
        """
        Тестируем команду ls.
        """
        # Выполним команду 'ls' и проверим вывод
        result = self.emulator.run_command('ls')
        self.assertIn('dir1', result)
        self.assertIn('dir2', result)

    def test_cd(self):
        """
        Тестируем команду cd.
        """
        # Перемещаемся в dir1 и проверяем, что текущая директория изменилась
        self.emulator.run_command('cd dir1')
        result = self.emulator.run_command('ls')
        self.assertIn('file1.txt', result)
        self.assertIn('file2.txt', result)

        # Пытаемся вернуться в корень
        self.emulator.run_command('cd ..')
        result = self.emulator.run_command('ls')
        self.assertIn('dir1', result)
        self.assertIn('dir2', result)

    def test_exit(self):
        """
        Тестируем команду exit.
        """
        with self.assertRaises(SystemExit):
            self.emulator.run_command('exit')

    def test_tree(self):
        """
        Тестируем команду tree.
        """
        result = self.emulator.run_command('tree')
        self.assertIn('dir1/', result)
        self.assertIn('file1.txt', result)
        self.assertIn('file2.txt', result)
        self.assertIn('dir2/', result)
        self.assertIn('file3.txt', result)

    def test_head(self):
        """
        Тестируем команду head.
        """
        # Проверяем вывод первых 10 строк из файла
        result = self.emulator.run_command('head dir1/file1.txt')
        self.assertEqual(result, 'file is empty')  # Исправлено ожидание

        # Проверка на отсутствие файла
        result = self.emulator.run_command('head non_existing_file.txt')
        self.assertEqual(result, 'head: non_existing_file.txt: No such file')

    def test_touch(self):
        """
        Тестируем команду touch.
        """
        # Проверяем, что файла нет до создания
        result = self.emulator.run_command('ls')
        self.assertNotIn('new_file.txt', result)

        # Создаем новый файл
        result = self.emulator.run_command('touch new_file.txt')
        self.assertEqual(result, 'touch: Created file new_file.txt')  # Исправлено ожидание

        # Проверяем, что файл появился
        result = self.emulator.run_command('ls')
        self.assertIn('new_file.txt', result)


if __name__ == '__main__':
    unittest.main()
