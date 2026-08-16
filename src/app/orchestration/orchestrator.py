from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.agents.architecture import ArchitectureAgent
from app.agents.base import Agent
from app.agents.brownfield import BrownfieldAgent
from app.agents.contracts import ContractAgent
from app.agents.database import DatabaseAgent
from app.agents.guarded import ImplementationBundleAgent
from app.agents.implementation import ImplementationAgent
from app.agents.planner import PlannerAgent
from app.agents.requirement import RequirementAgent
from app.agents.risk import RiskAgent
from app.agents.summary import SummaryAgent
from app.agents.testing import TestingAgent
from app.exceptions import ApprovalRequiredError, WorkflowError
from app.logging import event
from app.models import ApprovalDecision, Task, TaskStatus, WorkflowState
from app.validation.validator import EngineeringValidator

logger = logging.getLogger("agentic.workflow")


class WorkflowOrchestrator:
    def __init__(
        self,
        project_root: Path,
        output_dir: Path,
        max_retries: int = 2,
        approval_required: bool = True,
    ) -> None:
        self.project_root = project_root
        self.output_dir = output_dir
        self.max_retries = max_retries
        self.approval_required = approval_required
        self.agents: dict[str, Agent | None] = {
            "brownfield_scan": BrownfieldAgent(project_root),
            "analysis": RequirementAgent(),
            "architecture": ArchitectureAgent(),
            "api": ContractAgent(),
            "database": DatabaseAgent(),
            "implementation": ImplementationAgent(),
            "tests": TestingAgent(),
            "risks": RiskAgent(),
            "validation": None,
            "approval": None,
            "summary": SummaryAgent(),
        }
        self._bundle = ImplementationBundleAgent(output_dir)

    def _require_agent(self, task_id: str) -> Agent:
        agent = self.agents.get(task_id)
        if agent is None:
            raise WorkflowError(f"No agent configured for {task_id}")
        return agent

    async def run(
        self,
        requirement: str,
        mode: str = "greenfield",
        auto_approve: bool = False,
    ) -> WorkflowState:
        state = WorkflowState(requirement=requirement, mode=mode)
        plan = await PlannerAgent().execute(state)
        self._load_tasks(state, plan["tasks"])
        self._record(state, "planner", "completed", "Task graph created")
        await self._execute_graph(state)
        if state.validation is None:
            raise WorkflowError("Validation did not execute")
        if not state.validation.passed:
            details = "; ".join(state.validation.failures)
            raise WorkflowError(f"Engineering validation failed: {details}")
        approval = ApprovalDecision.APPROVED if auto_approve else None
        if self.approval_required and approval is None:
            state.tasks["approval"].status = TaskStatus.REQUIRES_APPROVAL
            self._record(
                state,
                "approval",
                "requires_approval",
                "Human approval required before finalization",
            )
            raise ApprovalRequiredError(state.workflow_id)
        state.approval = approval or ApprovalDecision.APPROVED
        state.tasks["approval"].status = TaskStatus.APPROVED
        self._record(state, "approval", "approved", "Approval recorded")
        result = await self._require_agent("summary").execute(state)
        state.artifacts.update(result)
        state.tasks["summary"].status = TaskStatus.COMPLETED
        state.completed_at = datetime.now(UTC)
        self._record(
            state,
            "summary",
            "completed",
            "Final engineering summary generated",
        )
        return state

    async def revise_and_resume(
        self,
        state: WorkflowState,
        feedback: str,
    ) -> WorkflowState:
        """Route a rejected workflow back into planning and execution."""
        if state.approval not in {
            ApprovalDecision.REJECTED,
            ApprovalDecision.NEEDS_REVISION,
        }:
            raise WorkflowError("Revision requires a rejected or needs-revision approval decision")
        state.approval = None
        state.completed_at = None
        state.artifacts["revision_feedback"] = feedback
        self._record(state, "human", "revision_requested", feedback)

        plan = await PlannerAgent().execute(state)
        state.tasks.clear()
        self._load_tasks(state, plan["tasks"])
        state.validation = None
        self._record(state, "planner", "replanned", "Workflow replanned after human feedback")
        await self._execute_graph(state)
        if state.validation is None or not state.validation.passed:
            raise WorkflowError("Revised engineering validation failed")
        return state

    async def approve_and_finalize(
        self,
        state: WorkflowState,
        decision: ApprovalDecision,
    ) -> WorkflowState:
        if state.validation is None or not state.validation.passed:
            raise WorkflowError("Cannot approve an unvalidated workflow")
        if decision != ApprovalDecision.APPROVED:
            state.approval = decision
            state.tasks["approval"].status = TaskStatus.REJECTED
            self._record(
                state,
                "approval",
                decision.value.lower(),
                "Approval rejected; workflow requires revision",
            )
            return state
        state.approval = decision
        state.tasks["approval"].status = TaskStatus.APPROVED
        result = await self._require_agent("summary").execute(state)
        state.artifacts.update(result)
        state.tasks["summary"].status = TaskStatus.COMPLETED
        state.completed_at = datetime.now(UTC)
        self._record(
            state,
            "summary",
            "completed",
            "Final engineering summary generated",
        )
        return state

    @staticmethod
    def _load_tasks(state: WorkflowState, tasks: list[Task]) -> None:
        for task in tasks:
            state.tasks[task.id] = task

    async def _execute_graph(self, state: WorkflowState) -> None:
        while True:
            pending = [
                task
                for task in state.tasks.values()
                if task.id not in {"approval", "summary"}
                and task.status in {TaskStatus.PENDING, TaskStatus.RETRYING}
            ]
            if not pending:
                break
            ready = [
                task
                for task in pending
                if all(
                    state.tasks[dependency].status == TaskStatus.COMPLETED
                    for dependency in task.dependencies
                )
            ]
            if not ready:
                blocked = [
                    task
                    for task in pending
                    if any(
                        state.tasks[dependency].status in {TaskStatus.FAILED, TaskStatus.REJECTED}
                        for dependency in task.dependencies
                    )
                ]
                for task in blocked:
                    task.status = TaskStatus.BLOCKED
                raise WorkflowError("No executable tasks remain; dependency graph is blocked")
            await asyncio.gather(*(self._run_task(state, task) for task in ready))

    async def _run_task(self, state: WorkflowState, task: Task) -> None:
        task.status = TaskStatus.RUNNING
        self._record(state, task.id, "running", task.title)
        try:
            if task.id == "implementation":
                result = await self._bundle.execute(state)
                result.update(await self._require_agent("implementation").execute(state))
            elif task.id == "validation":
                result = {"validation": EngineeringValidator().validate(state, self.project_root)}
            elif task.id == "approval":
                task.status = TaskStatus.REQUIRES_APPROVAL
                self._record(
                    state,
                    task.id,
                    "requires_approval",
                    "Waiting for human approval",
                )
                return
            else:
                result = await self._require_agent(task.id).execute(state)
            self._merge_result(state, result)
            task.status = TaskStatus.COMPLETED
            task.error = None
            self._record(state, task.id, "completed", task.title)
        except Exception as exc:
            task.retries += 1
            task.error = str(exc)
            if task.retries <= self.max_retries:
                task.status = TaskStatus.RETRYING
                self._record(
                    state,
                    task.id,
                    "retrying",
                    str(exc),
                    retry_count=task.retries,
                )
            else:
                task.status = TaskStatus.FAILED
                state.errors.append(f"{task.id}: {exc}")
                self._record(
                    state,
                    task.id,
                    "failed",
                    str(exc),
                    retry_count=task.retries,
                )
                raise

    @staticmethod
    def _merge_result(state: WorkflowState, result: dict[str, Any]) -> None:
        for key, value in result.items():
            if key == "analysis":
                state.analysis = value
            elif key == "architecture":
                state.architecture = value
            elif key == "validation":
                state.validation = value
            elif key == "tasks":
                for task in value:
                    state.tasks[task.id] = task
            elif key == "artifacts" and isinstance(value, dict):
                state.artifacts.update(value)
            else:
                state.artifacts[key] = value

    @staticmethod
    def _record(
        state: WorkflowState,
        actor: str,
        status: str,
        message: str,
        **extra: Any,
    ) -> None:
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "actor": actor,
            "status": status,
            "message": message,
            **extra,
        }
        state.history.append(entry)
        event(
            logger,
            workflow_id=state.workflow_id,
            actor=actor,
            status=status,
            message=message,
            **extra,
        )
