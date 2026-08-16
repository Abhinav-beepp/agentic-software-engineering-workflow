from typing import Any

from app.agents.base import Agent
from app.models import WorkflowState


class ImplementationAgent(Agent):
    name = "implementation"

    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        return {
            "implementation": {
                "modules": [
                    "app.main",
                    "app.api.url_routes",
                    "app.services.url_service",
                    "app.storage.repository",
                    "app.storage.models",
                ],
                "guardrails": [
                    "HTTP(S) URL validation",
                    "unique short-code constraint",
                    "bounded collision retry",
                    "structured error responses",
                ],
            }
        }
