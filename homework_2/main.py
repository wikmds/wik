import yaml
import requests
import graphviz
import xml.etree.ElementTree as ET
from collections import defaultdict


class DependencyVisualizer:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)

        self.graphviz_path = self.config["graphviz_path"]
        self.repository_url = self.config["repository_url"]
        self.main_package = self.config["package_name"]
        self.output_file = self.config["output_file"]
        self.dependencies = defaultdict(list)

    def fetch_dependencies(self, group_id, artifact_id, version, depth=3):
        if depth == 0:
            return
        group_path = group_id.replace('.', '/')
        pom_url = f"{self.repository_url}{group_path}/{artifact_id}/{version}/{artifact_id}-{version}.pom"
        print(f"Fetching dependencies from: {pom_url}")

        try:
            response = requests.get(pom_url)
            if response.status_code == 200:
                xml_data = response.text
                dependencies_found = self.parse_dependencies(xml_data)
                for dep_group_id, dep_artifact_id, dep_version in dependencies_found:
                    dep_full = f"{dep_group_id}:{dep_artifact_id}:{dep_version}"
                    self.dependencies[f"{group_id}:{artifact_id}:{version}"].append(dep_full)
                    self.fetch_dependencies(dep_group_id, dep_artifact_id, dep_version, depth-1)
            else:
                print(f"Could not fetch dependencies: {response.status_code}")
        except Exception as e:
            print(f"Error fetching dependencies: {e}")

    def parse_dependencies(self, xml_data):
        dependencies = []
        try:
            root = ET.fromstring(xml_data)
            namespace = {"m": "http://maven.apache.org/POM/4.0.0"}

            for dependency in root.findall(".//m:dependencies/m:dependency", namespaces=namespace):
                group_id = dependency.find("m:groupId", namespaces=namespace).text
                artifact_id = dependency.find("m:artifactId", namespaces=namespace).text
                version_element = dependency.find("m:version", namespaces=namespace)
                version = version_element.text if version_element is not None else "UNKNOWN"
                dependencies.append((group_id, artifact_id, version))

        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
        return dependencies

    def generate_graph(self):
        graph = graphviz.Digraph(comment="Dependency Graph", format="png")

        for key, deps in self.dependencies.items():
            source_artifact, source_version = key.split(':')[1], key.split(':')[2]
            source_name = f"{source_artifact} {source_version}"

            for dep in deps:
                _, dep_artifact_id, dep_version = dep.split(':')
                target_name = f"{dep_artifact_id} {dep_version}"
                graph.edge(source_name, target_name)
        return graph

    def visualize(self):
        group_id, artifact_id, version = self.main_package.split(':')
        self.fetch_dependencies(group_id, artifact_id, version)

        graph = self.generate_graph()
        graph.render(filename=self.output_file, cleanup=True, directory=".")
        print(f"Graph generated and saved to {self.output_file}")


if __name__ == "__main__":
    visualizer = DependencyVisualizer("config.yaml")
    visualizer.visualize()
