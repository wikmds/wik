import unittest
from unittest.mock import patch
import sys
import json
from main import ConfigParser, ParsingError


class TestConfigParser(unittest.TestCase):
    # Тест 1: Проверяем, что константы обрабатываются корректно
    def test_constants(self):
        input_lines = [
            "set speed = 10",
            "let = .(speed + 12).",
            "actions = [\"move\", \"turn\", \"stop\"]"
        ]
        parser = ConfigParser()
        result = parser.parse(input_lines)

        expected_output = {
            "let": 22,
            "actions": ["move", "turn", "stop"]
        }

        self.assertEqual(result, expected_output)

    # Тест 2: Проверяем вложенные словари
    def test_nested_dictionaries(self):
        input_lines = [
            "parameters = {",
            "    max_load => 100,",
            "    tolerance => 12,",
            "    parameters1 => {",
            "        max_load1 => 100,",
            "        tolerance1 => 12",
            "    }",
            "}"
        ]
        parser = ConfigParser()
        result = parser.parse(input_lines)

        expected_output = {
            "parameters": {
                "max_load": 100,
                "tolerance": 12,
                "max_load1": 100,
                "tolerance1": 12
            }
        }

        self.assertEqual(result, expected_output)

    # Тест 3: Проверяем вычисления abs и pow
    def test_math_operations(self):
        input_lines = [
            "set a = 5",
            "set b = 5",
            "let = .(abs(b) + pow(a, 2))."
        ]
        parser = ConfigParser()
        result = parser.parse(input_lines)

        expected_output = {
            "let": 30
        }

        self.assertEqual(result, expected_output)

    # Тест 4: Проверяем массивы
    def test_arrays(self):
        input_lines = [
            "actions = [\"start\", \"stop\", \"pause\"]"
        ]
        parser = ConfigParser()
        result = parser.parse(input_lines)

        expected_output = {
            "actions": ["start", "stop", "pause"]
        }

        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
