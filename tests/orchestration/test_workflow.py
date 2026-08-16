from pathlib import Path

import pytest

from app.models import ApprovalDecision, TaskStatus
from app.orchestration.orchestrator import WorkflowOrchestrator

MANDATORY_REQUIREMENT = (
    "Build a scalable URL shortener service with APIs, persistence, and analytics."
)


@pytest.mark.asyncio
async def test_workflow_runs_with_approval(tmp_path: Path) -> None:
    orchestrator = WorkflowOrchestrator(
        Path.cwd(),
        tmp_path / "artifacts",
        max_retries=1,
        approval_required=True,
    )
    state = await orchestrator.run(
        MANDATORY_REQUIREMENT,
        auto_approve=True,
    )
    assert state.validation is not None and state.validation.passed
    assert state.approval == ApprovalDecision.APPROVED
    assert state.tasks["summary"].status == TaskStatus.COMPLETED
    assert state.artifacts["engineering_summary"]["limitations"]


@pytest.mark.asyncio
async def test_workflow_pauses_for_human_approval(
    tmp_path: Path,
) -> None:
    orchestrator = WorkflowOrchestrator(
        Path.cwd(),
        tmp_path / "artifacts",
        max_retries=1,
        approval_required=True,
    )

    state = await orchestrator.run(
        MANDATORY_REQUIREMENT,
        auto_approve=False,
    )

    assert state.approval is None
    assert state.tasks["approval"].status == TaskStatus.REQUIRES_APPROVAL
    assert state.validation is not None
    assert state.validation.passed
    assert state.completed_at is None


@pytest.mark.asyncio
async def test_rejection_is_recorded(tmp_path: Path) -> None:
    orchestrator = WorkflowOrchestrator(
        Path.cwd(),
        tmp_path / "artifacts",
        max_retries=1,
        approval_required=True,
    )
    state = await orchestrator.run(
        MANDATORY_REQUIREMENT,
        auto_approve=True,
    )
    rejected = await orchestrator.approve_and_finalize(
        state,
        ApprovalDecision.REJECTED,
    )
    assert rejected.approval == ApprovalDecision.REJECTED
    assert rejected.tasks["approval"].status == TaskStatus.REJECTED


@pytest.mark.asyncio
async def test_rejection_can_trigger_replanning_and_recovery(
    tmp_path: Path,
) -> None:
    orchestrator = WorkflowOrchestrator(
        Path.cwd(),
        tmp_path / "artifacts",
        max_retries=1,
        approval_required=True,
    )
    state = await orchestrator.run(
        MANDATORY_REQUIREMENT,
        auto_approve=True,
    )
    rejected = await orchestrator.approve_and_finalize(
        state,
        ApprovalDecision.NEEDS_REVISION,
    )
    revised = await orchestrator.revise_and_resume(
        rejected,
        "Clarify analytics and preserve the existing API contract.",
    )
    assert revised.validation is not None and revised.validation.passed
    assert revised.approval is None
    assert revised.artifacts["revision_feedback"]
    assert any(h["status"] == "replanned" for h in revised.history)
