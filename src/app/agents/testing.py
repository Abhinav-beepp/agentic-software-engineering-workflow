from typing import Any

from app.agents.base import Agent
from app.models import WorkflowState


class TestingAgent(Agent):
    name = "testing"

    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        return {
            "test_plan": {
                "unit": [
                    "URL validation",
                    "short-code generation",
                    "collision handling",
                    "service behavior",
                ],
                "integration": [
                    "create",
                    "redirect",
                    "analytics",
                    "health",
                    "persistence",
                    "invalid/missing inputs",
                ],
                "orchestration": [
                    "dependency resolution",
                    "parallel ready tasks",
                    "retry",
                    "recovery",
                    "approval",
                ],
                "e2e": ["mandatory requirement through final engineering summary"],
            }
        }
