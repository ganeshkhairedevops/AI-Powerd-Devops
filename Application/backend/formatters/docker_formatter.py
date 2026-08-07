"""
Docker Formatter

Converts parsed Docker information into
beautiful GitHub Markdown.
"""

from typing import List, Dict


class DockerFormatter:

    def running_containers(self, containers: List[Dict]) -> str:

        if not containers:
            return """# ?? Docker Containers

No running containers found.
"""

        md = "# ?? Running Docker Containers\n\n"

        md += f"**Total Running Containers:** {len(containers)}\n\n"

        md += "| Name | Image | Status | Ports |\n"
        md += "|------|-------|--------|-------|\n"

        for c in containers:

            status = c.get("status", "")

            icon = "??"

            if "Exited" in status:
                icon = "??"

            elif "Restarting" in status:
                icon = "??"

            md += (
                f"| {c.get('name','-')} | "
                f"{c.get('image','-')} | "
                f"{icon} {status} | "
                f"{c.get('ports','-')} |\n"
            )

        md += """

---

## Suggested Commands

```bash
docker logs <container>
docker inspect <container>
docker stats
docker ps -a