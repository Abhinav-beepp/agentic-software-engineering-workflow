from pathlib import Path
from typing import Any

from app.agents.artifacts import ArtifactAgent
from app.agents.base import Agent
from app.agents.testing import TestingAgent
from app.models import WorkflowState


class ImplementationBundleAgent(Agent):
    name = "implementation-bundle"

    def __init__(self, output_dir: Path) -> None:
        self.artifact_agent = ArtifactAgent(output_dir)
        self.testing_agent = TestingAgent()

    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        result = await self.artifact_agent.execute(state)
        result.update(await self.testing_agent.execute(state))
        return result
