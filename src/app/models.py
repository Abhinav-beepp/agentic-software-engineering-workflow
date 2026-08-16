from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, HttpUrl


def utcnow() -> datetime:
    return datetime.now(UTC)


class TaskStatus(StrEnum):
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    BLOCKED = "BLOCKED"
    REQUIRES_APPROVAL = "REQUIRES_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class TaskType(StrEnum):
    ANALYSIS = "ANALYSIS"
    ARCHITECTURE = "ARCHITECTURE"
    API = "API"
    DATABASE = "DATABASE"
    IMPLEMENTATION = "IMPLEMENTATION"
    TEST = "TEST"
    DOCUMENTATION = "DOCUMENTATION"
    VALIDATION = "VALIDATION"
    SECURITY = "SECURITY"
    OBSERVABILITY = "OBSERVABILITY"


class ApprovalDecision(StrEnum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    NEEDS_REVISION = "NEEDS_REVISION"


class Task(BaseModel):
    id: str = Field(default_factory=lambda: f"task-{uuid4().hex[:8]}")
    title: str
    description: str
    type: TaskType
    priority: int = 3
    dependencies: list[str] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    expected_outputs: list[str] = Field(default_factory=list)
    validation_criteria: list[str] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    retries: int = 0
    error: str | None = None
    output_refs: list[str] = Field(default_factory=list)


class RequirementAnalysis(BaseModel):
    original_requirement: str
    intent: str
    functional_requirements: list[str]
    non_functional_requirements: list[str]
    constraints: list[str]
    assumptions: list[str]
    ambiguities: list[str]
    clarifying_questions: list[str]
    acceptance_criteria: list[str]
    normalized_problem: str


class ArchitectureDecision(BaseModel):
    overview: str
    components: list[str]
    data_flows: list[str]
    decisions: list[str]
    tradeoffs: list[str]


class ValidationResult(BaseModel):
    passed: bool
    checks: list[str]
    failures: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class WorkflowState(BaseModel):
    workflow_id: str = Field(default_factory=lambda: f"wf-{uuid4().hex[:12]}")
    requirement: str
    mode: str = "greenfield"
    tasks: dict[str, Task] = Field(default_factory=dict)
    artifacts: dict[str, Any] = Field(default_factory=dict)
    analysis: RequirementAnalysis | None = None
    architecture: ArchitectureDecision | None = None
    validation: ValidationResult | None = None
    approval: ApprovalDecision | None = None
    errors: list[str] = Field(default_factory=list)
    history: list[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utcnow)
    completed_at: datetime | None = None


class CreateURLRequest(BaseModel):
    original_url: HttpUrl


class CreateURLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    created_at: datetime


class AnalyticsResponse(BaseModel):
    short_code: str
    click_count: int
    created_at: datetime
    last_clicked_at: datetime | None
