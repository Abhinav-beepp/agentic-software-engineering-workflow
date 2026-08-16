from typing import Any

from app.agents.base import Agent
from app.models import WorkflowState


class ContractAgent(Agent):
    name = "api-contract"

    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        contract = {
            "POST /api/v1/urls": {
                "request": {"original_url": "string(uri)"},
                "response": {
                    "id": "integer",
                    "short_code": "string",
                    "short_url": "string",
                },
                "status": 201,
            },
            "GET /api/v1/urls/{short_code}/analytics": {
                "response": {
                    "short_code": "string",
                    "click_count": "integer",
                },
                "status": 200,
            },
            "GET /{short_code}": {
                "response": "307 redirect",
                "errors": [404],
            },
            "GET /health": {
                "response": {"status": "ok"},
                "status": 200,
            },
        }
        return {"api_contract": contract}
