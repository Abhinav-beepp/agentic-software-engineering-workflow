from pathlib import Path
from typing import Any

from app.agents.base import Agent
from app.models import WorkflowState


class BrownfieldAgent(Agent):
    name = "brownfield_scan"

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()

    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        files = [
            path.relative_to(self.project_root).as_posix()
            for path in self.project_root.rglob("*")
            if path.is_file()
        ]

        relevant_files = sorted(files)

        return {
            "brownfield_analysis": {
                "project_root": str(self.project_root),
                "file_count": len(files),
                "relevant_files": relevant_files,
                "observed_files": relevant_files,
                "directories": sorted(
                    {
                        path.relative_to(self.project_root).as_posix()
                        for path in self.project_root.rglob("*")
                        if path.is_dir()
                    }
                ),
                "requirement": state.requirement,
                "mode": "brownfield",
                "note": ("Analysis is based only on files observed in the supplied repository."),
            }
        }
