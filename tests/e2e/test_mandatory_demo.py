from pathlib import Path

import pytest

from app.orchestration.orchestrator import WorkflowOrchestrator

MANDATORY_REQUIREMENT = (
    "Build a scalable URL shortener service with APIs, persistence, and analytics."
)


@pytest.mark.asyncio
async def test_mandatory_url_shortener_requirement_end_to_end(
    tmp_path: Path,
) -> None:
    orchestrator = WorkflowOrchestrator(
        Path.cwd(),
        tmp_path / "artifacts",
        max_retries=2,
        approval_required=True,
    )
    state = await orchestrator.run(
        MANDATORY_REQUIREMENT,
        auto_approve=True,
    )
    assert state.analysis is not None
    assert state.architecture is not None
    assert state.validation is not None and state.validation.passed
    assert len(state.history) >= 10
    assert state.artifacts.get("engineering_summary")
