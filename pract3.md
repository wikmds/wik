# Практическое занятие №3. Конфигурационные языки

## Задача 1
Реализовать на `Jsonnet` приведенный ниже пример в формате `JSON`. Использовать в реализации свойство программируемости и принцип `DRY`.
```jsonnet
local groupCount = 24;
local studentData = [
  { age: 19, group: "ИКБО-4-20", name: "Иванов И.И." },
  { age: 18, group: "ИКБО-5-20", name: "Петров П.П." },
  { age: 18, group: "ИКБО-5-20", name: "Сидоров С.С." },
  { age: 19, group: "ИКБО-3-20", name: "Новиков Н.Н." }, // Пример добавленного студента
];

{
  groups: [
    "ИКБО-" + std.asString(i) + "-20" for i in std.range(1, groupCount)
  ],
  students: studentData,
  subject: "Конфигурационное управление",
}
```

## Задача 2
Реализовать на `Dhall` приведенный ниже пример в формате `JSON`. Использовать в реализации свойство программируемости и принцип `DRY`.
```dhall
let Prelude = https://prelude.dhall-lang.org/v20.2.0/package.dhall

let Group = Text

let Student = { age : Natural, group : Group, name : Text }

let Example =
      { groups : List Group
      , students : List Student
      , subject : Text
      }

let groups =
      Prelude.List.generate 24 (\(i : Natural) -> "ИКБО-${Natural/show (i + 1)}-20" : Text)

let students : List Student =
      [ { age = 19, group = "ИКБО-4-20", name = "Иванов И.И." }
      , { age = 18, group = "ИКБО-5-20", name = "Петров П.П." }
      , { age = 18, group = "ИКБО-5-20", name = "Сидоров С.С." }
      , { age = 19, group = "ИКБО-3-20", name = "Новиков Н.Н." }  -- добавленный студент
      ]

let subject = "Конфигурационное управление"

in  { groups = groups, students = students, subject = subject } : Example
```

# `#`
Для решения дальнейших задач потребуется программа на Питоне, представленная ниже.

```Python
import random

def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
E = a
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))

```

Реализовать грамматики, описывающие следующие языки (для каждого решения привести БНФ). Код решения должен содержаться в переменной BNF:

## Задача 3

Язык нулей и единиц.

```
import random

def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
E = 10 | 100 | 11 | 101101 | 000
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))
```

## Задача 4

Язык правильно расставленных скобок двух видов.

```
import random

def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
E = (E) | {E} | E E | ''
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))
```

## Задача 5

Язык выражений алгебры логики.

```
import random

def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
E = E & E | E | E | ~E | (E) | x | y
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))
```

## Полезные ссылки

Configuration complexity clock: https://mikehadlow.blogspot.com/2012/05/configuration-complexity-clock.html

Json: http://www.json.org/json-ru.html

Язык Jsonnet: https://jsonnet.org/learning/tutorial.html

Язык Dhall: https://dhall-lang.org/

Учебник в котором темы построения синтаксических анализаторов (БНФ, Lex/Yacc) изложены подробно: https://ita.sibsutis.ru/sites/csc.sibsutis.ru/files/courses/trans/LanguagesAndTranslationMethods.pdf

Полезные материалы для разработчика (очень рекомендую посмотреть слайды и прочие ссылки, все это актуально и для других тем нашего курса): https://habr.com/ru/company/JetBrains-education/blog/547768/
