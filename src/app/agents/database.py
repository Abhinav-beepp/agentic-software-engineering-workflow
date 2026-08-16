from typing import Any

from app.agents.base import Agent
from app.models import WorkflowState


class DatabaseAgent(Agent):
    name = "database-design"

    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        return {
            "database_schema": {
                "urls": [
                    "id",
                    "original_url",
                    "short_code UNIQUE",
                    "created_at",
                    "updated_at",
                    "click_count",
                    "last_clicked_at",
                ],
                "click_events": [
                    "id",
                    "url_id FK",
                    "clicked_at",
                    "user_agent",
                    "referrer",
                ],
            }
        }
