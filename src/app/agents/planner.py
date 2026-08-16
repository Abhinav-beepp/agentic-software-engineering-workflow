from typing import Any

from app.agents.base import Agent
from app.models import Task, TaskType, WorkflowState


class PlannerAgent(Agent):
    name = "task-planner"

    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        tasks: list[Task] = []
        if state.mode == "brownfield":
            tasks.append(
                Task(
                    id="brownfield_scan",
                    title="Inspect existing codebase",
                    description=(
                        "Scan the supplied repository and identify observed impacted areas."
                    ),
                    type=TaskType.ANALYSIS,
                    expected_outputs=["brownfield_analysis"],
                    validation_criteria=["Only observed files are reported."],
                )
            )

        tasks.extend(
            [
                Task(
                    id="analysis",
                    title="Normalize requirement",
                    description=(
                        "Interpret intent, ambiguity, assumptions, and acceptance criteria."
                    ),
                    type=TaskType.ANALYSIS,
                    expected_outputs=["requirement_analysis"],
                    validation_criteria=[
                        "Analysis contains normalized problem and acceptance criteria."
                    ],
                ),
                Task(
                    id="architecture",
                    title="Design architecture",
                    description=(
                        "Define service boundaries, data model, API surface, and scaling path."
                    ),
                    type=TaskType.ARCHITECTURE,
                    dependencies=["analysis"],
                    expected_outputs=["architecture"],
                    validation_criteria=[
                        "Architecture names components, data flows, decisions, and trade-offs."
                    ],
                ),
                Task(
                    id="api",
                    title="Define API contract",
                    description=("Define endpoint behavior, request/response models, and errors."),
                    type=TaskType.API,
                    dependencies=["architecture"],
                    expected_outputs=["api_contract"],
                    validation_criteria=[
                        "API contract includes create, analytics, redirect, and health behavior."
                    ],
                ),
                Task(
                    id="database",
                    title="Design persistence",
                    description="Define URL and analytics persistence model.",
                    type=TaskType.DATABASE,
                    dependencies=["architecture"],
                    expected_outputs=["database_schema"],
                    validation_criteria=["Schema supports unique short codes and click analytics."],
                ),
                Task(
                    id="implementation",
                    title="Implement service",
                    description=(
                        "Build the runnable URL shortener and supporting workflow artifacts."
                    ),
                    type=TaskType.IMPLEMENTATION,
                    dependencies=["api", "database"],
                    expected_outputs=["implementation"],
                    validation_criteria=["Application imports and core API behavior executes."],
                ),
                Task(
                    id="tests",
                    title="Generate and execute tests",
                    description=(
                        "Cover unit, API integration, orchestration, and end-to-end paths."
                    ),
                    type=TaskType.TEST,
                    dependencies=["implementation"],
                    expected_outputs=["test_plan"],
                    validation_criteria=["Required test suites exist and pass."],
                ),
                Task(
                    id="risks",
                    title="Assess risks and trade-offs",
                    description=(
                        "Identify failure modes, risks, mitigations, "
                        "assumptions, and evolution path."
                    ),
                    type=TaskType.SECURITY,
                    dependencies=["architecture", "implementation"],
                    expected_outputs=["risk_register"],
                    validation_criteria=["Risks include mitigations and explicit trade-offs."],
                ),
                Task(
                    id="validation",
                    title="Validate engineering outcome",
                    description=(
                        "Run deterministic checks over artifacts, tests, and workflow state."
                    ),
                    type=TaskType.VALIDATION,
                    dependencies=["tests", "risks"],
                    expected_outputs=["validation"],
                    validation_criteria=["All mandatory artifacts and checks pass."],
                ),
                Task(
                    id="approval",
                    title="Human approval gate",
                    description=("Require an explicit approval decision before finalization."),
                    type=TaskType.VALIDATION,
                    dependencies=["validation"],
                    expected_outputs=["approval"],
                    validation_criteria=["Approval decision is recorded."],
                ),
                Task(
                    id="summary",
                    title="Produce engineering summary",
                    description=(
                        "Create final implementation plan, artifacts, risks, "
                        "validation, assumptions, and limitations."
                    ),
                    type=TaskType.DOCUMENTATION,
                    dependencies=["approval"],
                    expected_outputs=["engineering_summary"],
                    validation_criteria=["Summary contains all required sections."],
                ),
            ]
        )
        return {"tasks": tasks}
