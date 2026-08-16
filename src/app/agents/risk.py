from typing import Any

from app.agents.base import Agent
from app.models import WorkflowState


class RiskAgent(Agent):
    name = "risk-analysis"

    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        risks = [
            {
                "risk": "SQLite write contention",
                "impact": "medium",
                "mitigation": "Use PostgreSQL for multi-instance production deployment.",
            },
            {
                "risk": "Short-code collision",
                "impact": "low",
                "mitigation": "Unique index plus bounded retry.",
            },
            {
                "risk": "Analytics growth",
                "impact": "medium",
                "mitigation": (
                    "Move click events to an append-only/event pipeline when volume warrants it."
                ),
            },
            {
                "risk": "Model-generated engineering output may be incorrect",
                "impact": "high",
                "mitigation": ("Deterministic validation, tests, guardrails, and human approval."),
            },
        ]
        return {
            "risks": risks,
            "tradeoffs": [
                "SQLite simplifies setup but is not the final choice for high write concurrency.",
                "Basic analytics avoids unnecessary event-stream infrastructure in the prototype.",
                (
                    "The deterministic provider favors reproducibility over "
                    "open-ended model creativity."
                ),
            ],
        }
