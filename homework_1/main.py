import os
import tarfile
import tkinter as tk
from tkinter import scrolledtext
import json


class Emulator:
    """
    Класс для эмуляции файловой системы и выполнения команд, аналогичных shell-командам.
    """

    def __init__(self, config_path):
        """
        Инициализация эмулятора, чтение конфигурации.
        """
        self.vfs_path = self.read_config(config_path)
        self.current_dir = ''
        self.previous_dirs = []
        self.init_vfs()

    def read_config(self, config_path):
        """
        Читает конфигурационный файл JSON и возвращает путь до виртуальной ФС.
        """
        with open(config_path, 'r') as file:
            config = json.load(file)
            return config['vfs_path']

    def init_vfs(self):
        """
        Инициализирует виртуальную файловую систему: открывает TAR-архив.
        """
        self.tar_ref = tarfile.open(self.vfs_path, 'r')

    def cleanup(self):
        """
        Очищает временные ресурсы.
        """
        self.tar_ref.close()

    def run_command(self, command, output_widget=None):
        """
        Выполняет указанную команду и выводит результат.
        """
        parts = command.split()
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        if output_widget:
            output_widget.insert(tk.END, f"{self.whoami()}$ {command}\n")

        if cmd == 'ls':
            result = self.ls()
        elif cmd == 'cd':
            result = self.cd(args[0]) if args else "cd: missing path"
        elif cmd == 'exit':
            self.cleanup()
            exit()
        elif cmd == 'uname':
            result = self.uname()
        elif cmd == 'tree':
            result = self.tree()
        elif cmd == 'head':
            result = self.head(args[0]) if args else "head: missing path"
        elif cmd == 'touch':
            result = self.touch(args[0]) if args else "touch: missing path"
        else:
            result = f"{cmd}: command not found"

        if output_widget:
            output_widget.insert(tk.END, result + "\n")
            output_widget.see(tk.END)

        return result

    def ls(self):
        """
        Выполняет команду 'ls': список файлов и директорий.
        """
        files = [f.name for f in self.tar_ref.getmembers() if f.name.startswith(self.current_dir)]
        current_dir_files = set()

        for f in files:
            relative_path = f.replace(self.current_dir, '', 1).lstrip('/')
            if '/' not in relative_path:
                current_dir_files.add(relative_path)
            else:
                dir_name = relative_path.split('/')[0]
                current_dir_files.add(dir_name)

        return "\n".join(sorted(current_dir_files))

    def cd(self, path):
        """
        Выполняет команду 'cd'.
        """
        if path == '..':
            if self.previous_dirs:
                self.current_dir = self.previous_dirs.pop()
            else:
                return "cd: ..: Already at the root directory"
        else:
            new_path = os.path.join(self.current_dir, path)
            if not new_path.endswith('/'):
                new_path += '/'
            if any(name.startswith(new_path) for name in [f.name for f in self.tar_ref.getmembers()]):
                self.previous_dirs.append(self.current_dir)
                self.current_dir = new_path
            else:
                return f"cd: {path}: No such file or directory"
        return f"Changed directory to {self.current_dir}"

    def uname(self):
        """
        Возвращает информацию об эмуляторе.
        """
        return "UnixEmulator"

    def tree(self, path=None, prefix=""):
        """
        Команда tree для отображения корректной иерархии файловой структуры.
        Теперь фильтрует вложенные элементы корректно.
        """
        if path is None:
            path = self.current_dir

        # Получаем все элементы, находящиеся на текущем уровне
        members = [
            f.name for f in self.tar_ref.getmembers()
            if f.name.startswith(path) and f.name != path
        ]

        # Оставляем только те элементы, которые находятся на текущем уровне
        dirs = set()
        files = set()
        for member in members:
            relative_path = member[len(path):].lstrip('/')
            # Только файлы или директории текущего уровня
            if '/' not in relative_path:
                if any(f.name.startswith(member + "/") for f in self.tar_ref.getmembers()):
                    dirs.add(relative_path)
                else:
                    files.add(relative_path)

        # Сортировка
        dirs = sorted(dirs)
        files = sorted(files)

        # Генерация результата
        result = ""
        for dir_name in dirs:
            result += f"{prefix}[+] {dir_name}\n"
            # Рекурсивный вызов
            result += self.tree(os.path.join(path, dir_name), prefix + "    ")

        for file_name in files:
            result += f"{prefix}- {file_name}\n"

        return result




    def head(self, path):
        """
        Выполняет команду 'head'.
        """
        try:
            file_path = os.path.join(self.current_dir, path)
            if file_path not in [f.name for f in self.tar_ref.getmembers()]:
                return f"head: {path}: No such file"

            member = self.tar_ref.getmember(file_path)
            file = self.tar_ref.extractfile(member)
            lines = file.readlines()
            if not lines:
                file.close()
                return "file is empty"
            file.close()

            return ''.join(line.decode('utf-8') for line in lines[:10])
        except Exception as e:
            return f"head: Error: {str(e)}"

    def touch(self, path):
        """
        Создаёт новый пустой файл и записывает его в новый TAR-архив.
        """
        try:
            new_tar_path = self.vfs_path + '.tmp'
            with tarfile.open(new_tar_path, 'w') as new_tar:
                # Копируем существующие файлы
                for member in self.tar_ref.getmembers():
                    file_obj = self.tar_ref.extractfile(member)
                    if file_obj:
                        new_tar.addfile(member, file_obj)
                    else:
                        new_tar.addfile(member)

                # Добавляем новый файл
                new_file_path = os.path.join(self.current_dir, path)
                new_file_info = tarfile.TarInfo(new_file_path)
                new_file_info.size = 0
                new_tar.addfile(new_file_info)

            # Заменяем старый TAR-архив новым
            self.tar_ref.close()
            os.replace(new_tar_path, self.vfs_path)
            self.init_vfs()

            return f"touch: Created file {path}"
        except Exception as e:
            return f"touch: Error: {str(e)}"

    def whoami(self):
        """
        Возвращает текущего пользователя.
        """
        return os.getlogin()


class ShellGUI:
    """
    Класс GUI оболочки.
    """
    def __init__(self, emulator):
        self.emulator = emulator
        self.root = tk.Tk()
        self.root.title("Shell Emulator")
        self.output = scrolledtext.ScrolledText(self.root, height=20, width=80, state=tk.NORMAL)
        self.output.pack()
        self.entry = tk.Entry(self.root, width=80)
        self.entry.pack()
        self.entry.bind('<Return>', self.execute_command)

    def execute_command(self, event):
        command = self.entry.get()
        self.emulator.run_command(command, output_widget=self.output)
        self.entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    config_path = 'config.json'
    emulator = Emulator(config_path)
    gui = ShellGUI(emulator)
    gui.run()
