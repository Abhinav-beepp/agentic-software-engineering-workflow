from typing import Any

from app.agents.base import Agent
from app.models import RequirementAnalysis, WorkflowState


class RequirementAgent(Agent):
    name = "requirement-analysis"

    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        req = state.requirement.strip()
        lower = req.lower()
        is_url_shortener = "url shortener" in lower or "url-shortener" in lower
        ambiguous = state.mode == "ambiguous" or "scalable" in lower or len(req.split()) < 8
        brownfield = state.mode == "brownfield"

        if is_url_shortener:
            intent = (
                "Transform the URL-shortener requirement into a reviewable, "
                "testable engineering plan and implementation."
            )
            functional = [
                "Create shortened URLs from valid HTTP(S) destinations.",
                "Persist URL mappings and resolve short codes to destinations.",
                "Record basic click analytics for redirects.",
                "Expose documented HTTP APIs and a health endpoint.",
            ]
            normalized = (
                "Design a modular URL-shortening service with an HTTP API, durable "
                "URL mapping, redirect-time analytics, validation, tests, and a "
                "documented path to higher-scale deployment."
            )
            acceptance = [
                "A valid URL can be shortened and persisted.",
                "A short code redirects to the original URL and increments click analytics.",
                "Invalid and unknown inputs return appropriate HTTP errors.",
                "Unit and integration tests validate core behavior.",
            ]
        else:
            intent = (
                "Convert the supplied software requirement into explicit engineering "
                "work while preserving uncertainty."
            )
            functional = [
                "Identify the requested user/system capabilities and affected interfaces."
            ]
            normalized = req
            acceptance = [
                "The requirement is decomposed into verifiable engineering tasks.",
                "Open questions and assumptions are visible before implementation is finalized.",
            ]

        if brownfield:
            normalized = f"Analyze the existing repository and plan the requested change: {req}"
            functional = [
                "Inspect the existing repository before proposing implementation changes.",
                "Identify impacted API, service, configuration, persistence, and test areas.",
                (
                    "Add the requested capability while preserving existing "
                    "behavior through regression tests."
                ),
            ]
            acceptance = [
                "Only observed repository structure is used as evidence.",
                "Impacted components and regression tests are identified.",
                "The requested change has explicit validation criteria.",
            ]

        ambiguities: list[str] = []
        questions: list[str] = []
        if ambiguous:
            ambiguities = [
                "Target peak requests per second are unspecified.",
                "Latency and availability SLOs are unspecified.",
                "Read/write workload shape is unspecified.",
                "Analytics retention/privacy requirements are unspecified.",
                "Geographic distribution and deployment scope are unspecified.",
            ]
            questions = [
                "What peak requests per second should the service support?",
                "What p95/p99 latency target and availability SLO are required?",
                "What is the expected read/write ratio and analytics volume?",
                "Is multi-region deployment required?",
                "What retention and privacy requirements apply to analytics?",
            ]

        return {
            "analysis": RequirementAnalysis(
                original_requirement=req,
                intent=intent,
                functional_requirements=functional,
                non_functional_requirements=[
                    "Maintainable modular design.",
                    "Reliable persistence and deterministic validation.",
                    "Explicit assumptions and measurable acceptance criteria.",
                ],
                constraints=["Prototype should run locally without mandatory paid services."],
                assumptions=[
                    "SQLite is acceptable for the local demonstration; PostgreSQL "
                    "is the production evolution path.",
                    "The prototype prioritizes demonstrability over production-scale "
                    "infrastructure.",
                ],
                ambiguities=ambiguities,
                clarifying_questions=questions,
                acceptance_criteria=acceptance,
                normalized_problem=normalized,
            )
        }
