from typing import Any

from app.agents.base import Agent
from app.models import ArchitectureDecision, WorkflowState


class ArchitectureAgent(Agent):
    name = "architecture"

    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        architecture = ArchitectureDecision(
            overview=(
                "A modular FastAPI service backed by SQLAlchemy, with a "
                "deterministic agent orchestrator around the engineering lifecycle. "
                "The URL service is separated from persistence and API adapters."
            ),
            components=[
                "FastAPI HTTP layer",
                "URLService domain/application service",
                "SQLAlchemy repository and models",
                "Agent abstractions and workflow state",
                "DAG-based orchestrator with retries and recovery",
                "Deterministic validator",
                "Human approval gate",
                "Artifact/document generator",
            ],
            data_flows=[
                "Create URL: HTTP -> URLService -> URLRepository -> "
                "SQLite/PostgreSQL-compatible persistence.",
                "Redirect: HTTP -> URLService -> URLRepository -> click event + redirect response.",
                "Engineering workflow: requirement -> analysis -> task graph -> "
                "dependent agents -> validation -> approval -> summary.",
            ],
            decisions=[
                "Use FastAPI for typed APIs and generated OpenAPI documentation.",
                "Use SQLite for a zero-friction local demo and preserve "
                "SQLAlchemy portability for PostgreSQL.",
                "Use deterministic validation for checks that should not depend on model behavior.",
                "Use an LLM provider interface so a real model can be added "
                "without coupling the workflow core.",
            ],
            tradeoffs=[
                "SQLite simplifies setup but is not the final choice for high write concurrency.",
                "Basic analytics avoids unnecessary event-stream infrastructure in the prototype.",
                "The deterministic provider favors reproducibility over "
                "open-ended model creativity.",
            ],
        )
        return {"architecture": architecture}
