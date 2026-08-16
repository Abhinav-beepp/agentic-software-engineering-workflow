from datetime import UTC, datetime
from typing import Any

from app.agents.base import Agent
from app.models import ApprovalDecision, WorkflowState


class SummaryAgent(Agent):
    name = "engineering-summary"

    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        if state.approval != ApprovalDecision.APPROVED:
            raise RuntimeError("Final summary requires approved workflow")
        summary = {
            "original_requirement": state.requirement,
            "implementation_plan": (state.analysis.normalized_problem if state.analysis else ""),
            "requirement_analysis": (state.analysis.model_dump() if state.analysis else {}),
            "architecture": (state.architecture.model_dump() if state.architecture else {}),
            "generated_artifacts": state.artifacts.get(
                "artifact_manifest",
                state.artifacts.get("generated_files", []),
            ),
            "validation": (state.validation.model_dump() if state.validation else {}),
            "risks": state.artifacts.get("risks", []),
            "tradeoffs": state.artifacts.get("tradeoffs", []),
            "assumptions": (state.analysis.assumptions if state.analysis else []),
            "limitations": [
                "Prototype uses SQLite locally.",
                "Analytics are intentionally basic.",
                "Authentication, rate limiting, expiration, and custom aliases "
                "are outside the mandatory scope.",
            ],
            "generated_at": datetime.now(UTC).isoformat(),
        }
        return {"engineering_summary": summary}
