import sys
import re
import json


class ParsingError(Exception):
    """Кастомное исключение для ошибок парсинга."""


class ConfigParser:
    def __init__(self):
        self.constants = {}

    # Основной метод парсинга
    def parse(self, lines):
        result = {}
        full_text = "\n".join(lines)
        result.update(self.handle_dictionaries(full_text))

        for line in lines:
            line = line.strip()
            if not line or line.startswith("||"):
                continue

            # Проверяем объявления констант
            if line.startswith("set "):
                self.handle_constant(line)
            # Проверяем переменные и вычисления
            elif "=" in line and not line.endswith("{"):
                # Проверяем, это не словарь
                if "=>" not in line:
                    result.update(self.handle_assignment(line))

        return result

    # Обработка объявления констант
    def handle_constant(self, line):
        match = re.match(r"set\s+([a-zA-Z][a-zA-Z0-9]*)\s*=\s*(\d+)", line)
        if match:
            name, value = match.groups()
            self.constants[name] = int(value)
        else:
            raise ParsingError(f"Invalid constant declaration: {line}")

    # Обработка вычислений и массивов
    def handle_assignment(self, line):
        # Обрабатываем вычисления типа .(speed + 12).
        match = re.match(r"([a-zA-Z][a-zA-Z0-9]*)\s*=\s*\.\((.*?)\)\.", line)
        if match:
            name, expr = match.groups()
            try:
                value = eval(expr, {"pow": pow, "abs": abs}, self.constants)
                return {name: value}
            except Exception as e:
                raise ParsingError(f"Error evaluating expression '{expr}': {e}")

        # Обрабатываем массивы
        match = re.match(r"([a-zA-Z][a-zA-Z0-9]*)\s*=\s*(\[.*\])", line)
        if match:
            name, array_expr = match.groups()
            try:
                value = json.loads(array_expr)
                return {name: value}
            except Exception as e:
                raise ParsingError(f"Error parsing array '{array_expr}': {e}")

        raise ParsingError(f"Invalid assignment: {line}")

    # Генерал-интерфейс для поиска словарей
    def handle_dictionaries(self, text):
        pattern = r"([a-zA-Z][a-zA-Z0-9]*)\s*=\s*\{(.*?)\}"
        matches = re.finditer(pattern, text, re.DOTALL)

        result = {}
        for match in matches:
            name, dict_body = match.groups()
            try:
                result[name] = self.parse_dictionary(dict_body)
            except ParsingError as e:
                raise ParsingError(f"Error parsing dictionary '{name}': {e}")

        return result

    # Парсим словарь и обрабатываем вложенные словари рекурсивно
    def parse_dictionary(self, body):
        result = {}
        pattern = r"([a-zA-Z][a-zA-Z0-9_]*)\s*=>\s*(\{.*\}|\[.*\]|\d+(\.\d+)?)"
        matches = re.finditer(pattern, body)

        for match in matches:
            key = match.group(1)
            value = match.group(2).strip()

            try:
                # Проверяем вложенный словарь
                if value.startswith("{") and value.endswith("}"):
                    result[key] = self.parse_dictionary(value[1:-1].strip())
                # Проверяем массивы
                elif value.startswith("[") and value.endswith("]"):
                    result[key] = json.loads(value)
                # Проверяем числа и вещественные числа
                elif re.match(r"^\d+(\.\d+)?$", value):
                    result[key] = float(value) if "." in value else int(value)
                else:
                    raise ParsingError(f"Invalid dictionary entry value '{value}' for key '{key}'")
            except Exception as e:
                raise ParsingError(f"Error parsing value '{value}' for dictionary key '{key}': {e}")

        return result


# Основной интерфейс для обработки аргументов и взаимодействия с пользователем
def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Считываем входные данные из файла
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()

        # Парсим входные данные
        parser = ConfigParser()
        parsed_data = parser.parse(lines)

        # Генерируем JSON и печатаем
        print("Parsed JSON output:")
        print(json.dumps(parsed_data, indent=4))

    except ParsingError as e:
        print(f"Parsing error: {e}")
    except FileNotFoundError:
        print("Error: Input file not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
