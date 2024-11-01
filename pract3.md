# Практическое занятие №3. Конфигурационные языки

## Задача 1
Реализовать на `Jsonnet` приведенный ниже пример в формате `JSON`. Использовать в реализации свойство программируемости и принцип `DRY`.
### Решение:
```jsonnet
{
  groups: ["ИКБО-1-20", "ИКБО-2-20", "ИКБО-3-20", "ИКБО-4-20", "ИКБО-5-20", 
           "ИКБО-6-20", "ИКБО-7-20", "ИКБО-8-20", "ИКБО-9-20", "ИКБО-10-20", 
           "ИКБО-11-20", "ИКБО-12-20", "ИКБО-13-20", "ИКБО-14-20", "ИКБО-15-20",
           "ИКБО-16-20", "ИКБО-17-20", "ИКБО-18-20", "ИКБО-19-20", "ИКБО-20-20", 
           "ИКБО-21-20", "ИКБО-22-20", "ИКБО-23-20", "ИКБО-24-20", "ИКБО-63-23"],

  students: [
    { name: "Иванов И.И.", age: 19, group: "ИКБО-4-20" },
    { name: "Петров П.П.", age: 20, group: "ИКБО-5-20" },
    { name: "Сидоров С.С.", age: 18, group: "ИКБО-6-20" },
    { name: "Козубова А.А.", age: 18, group: "ИКБО-63-23" },
  ]
}
```
### Результат:
![image](https://github.com/user-attachments/assets/7b2f83d1-845f-420b-b232-11fb8ebd8bea)


## Задача 2
Реализовать на `Dhall` приведенный ниже пример в формате `JSON`. Использовать в реализации свойство программируемости и принцип `DRY`.
### Решение:
```dhall
let Group = List Text
let Student = { age : Natural, group : Text, name : Text }

let studentsData = 
      { groups = [ "ИКБО-1-20", "ИКБО-2-20", "ИКБО-3-20", "ИКБО-4-20", "ИКБО-5-20",
                   "ИКБО-6-20", "ИКБО-7-20", "ИКБО-8-20", "ИКБО-9-20", "ИКБО-10-20",
                   "ИКБО-11-20", "ИКБО-12-20", "ИКБО-13-20", "ИКБО-14-20", "ИКБО-15-20",
                   "ИКБО-16-20", "ИКБО-17-20", "ИКБО-18-20", "ИКБО-19-20", "ИКБО-20-20",
                   "ИКБО-21-20", "ИКБО-22-20", "ИКБО-23-20", "ИКБО-24-20", "ИКБО-63-23" ] : Group,
      
        students = 
            [ { age = 19, group = "ИКБО-4-20", name = "Иванов И.И." }
            , { age = 20, group = "ИКБО-5-20", name = "Петров П.П." }
            , { age = 18, group = "ИКБО-6-20", name = "Сидоров С.С." }
            , { age = 18, group = "ИКБО-63-20", name = "Козубова А.А." }
            ] : List Student
      }

in studentsData
```
### Результат:
![image](https://github.com/user-attachments/assets/d1b7a7a8-99ab-441e-ab8c-e76e6c0405ec)


# `===`
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
### Решение:
```
BNF = '''
E = 10 | 100 | 11 | 101101 | 000
'''
```
### Результат:
![image](https://github.com/user-attachments/assets/3984e027-ed1c-47f9-bc13-90a3f5101d3a)



## Задача 4

Язык правильно расставленных скобок двух видов.
### Решение:
```
BNF = '''
E = (E) | {E} | E E | ''
'''
```

### Результат:
![image](https://github.com/user-attachments/assets/ea3a63e6-eeef-4663-aa34-ecd0990f312b)



## Задача 5
Язык выражений алгебры логики.

### Решение:
```
BNF = '''
E = E & E | E | E | ~E | (E) | x | y
'''
```
### Результат:
![image](https://github.com/user-attachments/assets/75e651d1-18a3-4b96-b1b2-bb847d961d44)



## Полезные ссылки

Configuration complexity clock: https://mikehadlow.blogspot.com/2012/05/configuration-complexity-clock.html

Json: http://www.json.org/json-ru.html

Язык Jsonnet: https://jsonnet.org/learning/tutorial.html

Язык Dhall: https://dhall-lang.org/

Учебник в котором темы построения синтаксических анализаторов (БНФ, Lex/Yacc) изложены подробно: https://ita.sibsutis.ru/sites/csc.sibsutis.ru/files/courses/trans/LanguagesAndTranslationMethods.pdf

Полезные материалы для разработчика (очень рекомендую посмотреть слайды и прочие ссылки, все это актуально и для других тем нашего курса): https://habr.com/ru/company/JetBrains-education/blog/547768/
