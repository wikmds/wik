import unittest
from unittest.mock import patch, mock_open, MagicMock
from main import DependencyVisualizer
import xml.etree.ElementTree as ET


class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        self.test_config = {
            "graphviz_path": "/usr/bin/graphviz",
            "repository_url": "https://repo1.maven.org/maven2/",
            "package_name": "org.springframework.boot:spring-boot-starter-web:3.4.0",
            "output_file": "dependency_graph"
        }

        # Mock open для конфигурационного файла
        self.mock_open = patch("builtins.open", mock_open(read_data=str(self.test_config))).start()

        # Создание экземпляра класса
        self.visualizer = DependencyVisualizer("config.yaml")

    def tearDown(self):
        patch.stopall()

    @patch("requests.get")
    def test_fetch_dependencies(self, mock_requests):
        # Мок сетевого запроса
        mocked_response = MagicMock()
        mocked_response.status_code = 200
        mocked_response.text = """
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <dependencies>
                <dependency>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-starter</artifactId>
                    <version>3.4.0</version>
                </dependency>
                <dependency>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-starter-json</artifactId>
                    <version>3.4.0</version>
                </dependency>
            </dependencies>
        </project>
        """
        mock_requests.return_value = mocked_response

        # Вызов метода
        self.visualizer.fetch_dependencies("org.springframework.boot", "spring-boot-starter-web", "3.4.0")

        # Проверяем, что зависимости были корректно загружены
        self.assertIn("org.springframework.boot:spring-boot-starter-web:3.4.0", self.visualizer.dependencies)
        self.assertIn("org.springframework.boot:spring-boot-starter:3.4.0", self.visualizer.dependencies["org.springframework.boot:spring-boot-starter-web:3.4.0"])
        self.assertIn("org.springframework.boot:spring-boot-starter-json:3.4.0", self.visualizer.dependencies["org.springframework.boot:spring-boot-starter-web:3.4.0"])

    def test_parse_dependencies(self):
        # XML-ответ
        xml_data = """
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <dependencies>
                <dependency>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-starter</artifactId>
                    <version>3.4.0</version>
                </dependency>
                <dependency>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-starter-json</artifactId>
                    <version>3.4.0</version>
                </dependency>
            </dependencies>
        </project>
        """
        # Тестируем парсер
        parsed_deps = self.visualizer.parse_dependencies(xml_data)
        expected_deps = [
            ("org.springframework.boot", "spring-boot-starter", "3.4.0"),
            ("org.springframework.boot", "spring-boot-starter-json", "3.4.0")
        ]

        self.assertListEqual(parsed_deps, expected_deps)

    @patch("graphviz.Digraph")
    def test_generate_graph(self, mock_graphviz):
        # Мок графвиз
        mock_digraph = mock_graphviz.return_value
        self.visualizer.dependencies = {
            "org.springframework.boot:spring-boot-starter-web:3.4.0": [
                "org.springframework.boot:spring-boot-starter:3.4.0",
                "org.springframework.boot:spring-boot-starter-json:3.4.0"
            ]
        }

        # Генерация графа
        graph = self.visualizer.generate_graph()
        mock_digraph.edge.assert_any_call("spring-boot-starter-web 3.4.0", "spring-boot-starter 3.4.0")
        mock_digraph.edge.assert_any_call("spring-boot-starter-web 3.4.0", "spring-boot-starter-json 3.4.0")

        self.assertIs(graph, mock_digraph)

    @patch("graphviz.Digraph")
    @patch("requests.get")
    def test_visualize(self, mock_requests, mock_graphviz):
        # Мок ответ для fetch_dependencies
        mocked_response = MagicMock()
        mocked_response.status_code = 200
        mocked_response.text = """
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <dependencies>
                <dependency>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-starter</artifactId>
                    <version>3.4.0</version>
                </dependency>
            </dependencies>
        </project>
        """
        mock_requests.return_value = mocked_response

        # Вызов visualize
        self.visualizer.visualize()

        # Проверяем, что fetch_dependencies и render были вызваны
        mock_graphviz.return_value.render.assert_called()


if __name__ == "__main__":
    unittest.main()
