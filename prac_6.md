## Задание 0
Визуализировать файл civgraph.txt.
```
dot -Tpng civgraph.txt -o civgraph.png
```
![civgraph](https://github.com/wikmds/wik/tree/main/images/civgraph.png) 

## Задание 1
Написать программу на Питоне, которая транслирует граф зависимостей civgraph в makefile в духе примера выше. Для мало знакомых с Питоном используется упрощенный вариант civgraph: civgraph.json.
```py
class CivGraphToMakefileConverter:
    def __init__(self, dependencies):
        """
        Конструктор класса. Принимает граф зависимостей в виде словаря.
        :param dependencies: Словарь зависимостей вида {'цель': ['зависимость1', 'зависимость2', ...]}
        """
        self.dependencies = dependencies

    def generate_makefile(self):
        makefile = []
        for target, deps in self.dependencies.items():
            makefile.append(f"{target}: {' '.join(deps)}")
            makefile.append(f"\t@echo Building {target}")
            makefile.append("")  # Пустая строка для разделения целей
        return "\n".join(makefile)

civgraph = {
    'all': ['main.o', 'util.o'],
    'main.o': ['main.c', 'util.h'],
    'util.o': ['util.c', 'util.h'],
    'clean': []
}

converter = CivGraphToMakefileConverter(civgraph)

makefile_content = converter.generate_makefile()

with open('Makefile', 'w') as f:
    f.write(makefile_content)

print("Makefile сгенерирован!")
```

```makefile
all: main.o util.o
	@echo Building all

main.o: main.c util.h
	@echo Building main.o

util.o: util.c util.h
	@echo Building util.o

clean: 
	@echo Building clean
```

## Задание 2
Реализовать вариант трансляции, при котором повторный запуск make не выводит для civgraph на экран уже выполненные "задачи".
```py
class CivGraphToMakefileConverter:
    def __init__(self, dependencies):
        self.dependencies = dependencies

    def generate_makefile(self):
        makefile = []
        for target, deps in self.dependencies.items():
            makefile.append(f"{target}: {' '.join(deps)}")
            makefile.append(f"\t@if [ ! -f {target} ] || [ {' -o '.join([f'{target} -ot {dep}' for dep in deps])} ]; then \\")
            makefile.append(f"\t\techo Building {target}; \\")
            makefile.append(f"\t\t# Здесь можно вставить команду для сборки {target}; \\")
            makefile.append("\tfi")
            makefile.append("") 
        return "\n".join(makefile)

civgraph = {
    'all': ['main.o', 'util.o'],
    'main.o': ['main.c', 'util.h'],
    'util.o': ['util.c', 'util.h'],
    'clean': []
}

converter = CivGraphToMakefileConverter(civgraph)

makefile_content = converter.generate_makefile()

with open('Makefile', 'w') as f:
    f.write(makefile_content)

print("Makefile сгенерирован!")
```

```makefile
all: main.o util.o
	@if [ ! -f all ] || [ all -ot main.o -o all -ot util.o ]; then \
		echo Building all; \
		# Здесь можно вставить команду для сборки all; \
	fi

main.o: main.c util.h
	@if [ ! -f main.o ] || [ main.o -ot main.c -o main.o -ot util.h ]; then \
		echo Building main.o; \
		# Здесь можно вставить команду для сборки main.o; \
	fi

util.o: util.c util.h
	@if [ ! -f util.o ] || [ util.o -ot util.c -o util.o -ot util.h ]; then \
		echo Building util.o; \
		# Здесь можно вставить команду для сборки util.o; \
	fi

clean: 
	@if [ ! -f clean ] || [  ]; then \
		echo Building clean; \
		# Здесь можно вставить команду для сборки clean; \
	fi
```


## Задание 3
Добавить цель clean, не забыв и про "животное".
```py
class CivGraphToMakefileConverter:
    def __init__(self, dependencies, objects):
        """
        Конструктор класса. Принимает граф зависимостей и список файлов для удаления в цели clean.
        :param dependencies: Словарь зависимостей вида {'цель': ['зависимость1', 'зависимость2', ...]}
        :param objects: Список объектов (например, .o файлов), которые будут удаляться в цели clean.
        """
        self.dependencies = dependencies
        self.objects = objects

    def generate_makefile(self):
        makefile = []

        for target, deps in self.dependencies.items():
            makefile.append(f"{target}: {' '.join(deps)}")
            makefile.append(f"\t@if [ ! -f {target} ] || [ {' -o '.join([f'{target} -ot {dep}' for dep in deps])} ]; then \\")
            makefile.append(f"\t\techo Building {target}; \\")
            makefile.append(f"\t\t# Здесь можно вставить команду для сборки {target}; \\")
            makefile.append("\tfi")
            makefile.append("")

        # clean
        makefile.append("clean:")
        makefile.append(f"\t@rm -f {' '.join(self.objects)}")
        makefile.append(f"\t@echo Cleaning complete. Мяу!")
        makefile.append("")

        return "\n".join(makefile)

civgraph = {
    'all': ['main.o', 'util.o'],
    'main.o': ['main.c', 'util.h'],
    'util.o': ['util.c', 'util.h'],
}

object_files = ['main.o', 'util.o']

converter = CivGraphToMakefileConverter(civgraph, object_files)

makefile_content = converter.generate_makefile()

with open('Makefile', 'w') as f:
    f.write(makefile_content)

print("Makefile сгенерирован!")
```

```makefile
all: main.o util.o
	@if [ ! -f all ] || [ all -ot main.o -o all -ot util.o ]; then \
		echo Building all; \
		# Здесь можно вставить команду для сборки all; \
	fi

main.o: main.c util.h
	@if [ ! -f main.o ] || [ main.o -ot main.c -o main.o -ot util.h ]; then \
		echo Building main.o; \
		# Здесь можно вставить команду для сборки main.o; \
	fi

util.o: util.c util.h
	@if [ ! -f util.o ] || [ util.o -ot util.c -o util.o -ot util.h ]; then \
		echo Building util.o; \
		# Здесь можно вставить команду для сборки util.o; \
	fi

clean:
	@rm -f main.o util.o
	@echo Cleaning complete.
```

## Задание 4
Написать makefile для следующего скрипта сборки:
```
gcc prog.c data.c -o prog
dir /B > files.lst
7z a distr.zip *.*
```
Вместо gcc можно использовать другой компилятор командной строки, но на вход ему должны подаваться два модуля: prog и data. Если используете не Windows, то исправьте вызовы команд на их эквиваленты из вашей ОС. В makefile должны быть, как минимум, следующие задачи: all, clean, archive. Обязательно покажите на примере, что уже сделанные подзадачи у вас не перестраиваются.
```makefile
# Компилятор и флаги
CC = gcc
CFLAGS = -Wall -O2

# Исходные файлы и объектный файл программы
SRC = prog.c data.c
OBJ = prog

# Файл со списком
FILES_LIST = files.lst

# Имя архива
ARCHIVE = distr.zip

# Задача по умолчанию
all: $(OBJ)

# Правило для сборки программы
$(OBJ): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(OBJ)

# Правило для создания архива
archive: $(OBJ) $(FILES_LIST)
	7z a $(ARCHIVE) *.*

# Правило для создания списка файлов
$(FILES_LIST): 
	ls > $(FILES_LIST)

# Очистка всех сгенерированных файлов
clean:
	rm -f $(OBJ) $(FILES_LIST) $(ARCHIVE)
```
