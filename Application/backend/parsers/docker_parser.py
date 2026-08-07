"""
Docker Output Parser

Converts docker CLI output into structured Python objects.
"""

from typing import List, Dict


class DockerParser:

    def parse_ps(self, output: str) -> List[Dict]:

        lines = output.strip().splitlines()

        if len(lines) <= 1:
            return []

        containers = []

        # Skip header
        for line in lines[1:]:

            parts = line.split()

            if len(parts) < 7:
                continue

            container = {
                "id": parts[0],
                "image": parts[1],
                "status": " ".join(parts[4:6]),
                "ports": parts[-2],
                "name": parts[-1],
            }

            containers.append(container)

        return containers


docker_parser = DockerParser()