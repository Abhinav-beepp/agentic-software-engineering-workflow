from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.agents.base import Agent
from app.models import WorkflowState


class ArtifactAgent(Agent):
    """Produce deterministic, reviewable engineering artifacts."""

    name = "artifact-generator"

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir

    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        analysis = state.analysis
        architecture = state.architecture

        api_contract = {
            "openapi": "3.0.3",
            "service": "URL Shortener",
            "endpoints": [
                {
                    "method": "POST",
                    "path": "/api/v1/urls",
                    "request": {"original_url": "string(uri)"},
                    "response": {
                        "id": "integer",
                        "short_code": "string",
                        "short_url": "string",
                    },
                    "status": 201,
                },
                {
                    "method": "GET",
                    "path": "/api/v1/urls/{short_code}/analytics",
                    "response": {
                        "short_code": "string",
                        "click_count": "integer",
                    },
                    "status": 200,
                },
                {
                    "method": "GET",
                    "path": "/{short_code}",
                    "response": "307 redirect",
                    "errors": [404],
                },
                {
                    "method": "GET",
                    "path": "/health",
                    "response": {"status": "ok"},
                    "status": 200,
                },
            ],
        }

        generated_service = '''"""Representative generated service artifact.

The real runnable implementation lives in src/app/services/url_service.py.
The workflow demonstrates code generation without executing untrusted source.
"""

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class ShortUrlDraft:
    original_url: str
    short_code: str


def validate_http_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("original_url must be an absolute HTTP(S) URL")
    return value


def build_short_url(base_url: str, short_code: str) -> str:
    return f"{base_url.rstrip('/')}/{short_code}"
'''

        generated_tests = '''"""Representative generated pytest examples."""

import pytest


def test_http_url_validation_accepts_https():
    from generated_code import validate_http_url

    assert validate_http_url("https://example.com/path") == (
        "https://example.com/path"
    )


def test_http_url_validation_rejects_non_http():
    from generated_code import validate_http_url

    with pytest.raises(ValueError):
        validate_http_url("ftp://example.com/file")
'''

        files = {
            "implementation_plan.md": (
                "# Implementation Plan\n\n"
                f"{analysis.normalized_problem if analysis else ''}\n\n"
                "## Rationale\n"
                "Use a small FastAPI service with a repository boundary around "
                "SQLAlchemy. Keep workflow orchestration independent from the "
                "runtime so the agent system can reason about other software "
                "requirements.\n\n"
                "## Assumptions\n"
                + "\n".join(f"- {item}" for item in (analysis.assumptions if analysis else []))
                + "\n\n## Ambiguities / Clarifying Questions\n"
                + "\n".join(
                    f"- {item}" for item in (analysis.clarifying_questions if analysis else [])
                )
                + "\n"
            ),
            "architecture.md": (
                "# Architecture\n\n"
                f"{architecture.overview if architecture else ''}\n\n"
                "## Components\n"
                + "\n".join(
                    f"- {item}" for item in (architecture.components if architecture else [])
                )
                + "\n\n## Data Flows\n"
                + "\n".join(
                    f"- {item}" for item in (architecture.data_flows if architecture else [])
                )
            ),
            "api_contract.json": json.dumps(api_contract, indent=2) + "\n",
            "database_schema.md": (
                "# Database Schema\n\n"
                "## urls\n"
                "- id\n- original_url\n- short_code (UNIQUE)\n"
                "- created_at\n- updated_at\n- click_count\n"
                "- last_clicked_at\n\n"
                "## click_events\n"
                "- id\n- url_id (FK urls.id)\n- clicked_at\n"
                "- user_agent\n- referrer\n"
            ),
            "test_plan.md": (
                "# Test Plan\n\n"
                "## Unit\n"
                "- URL validation\n"
                "- short-code generation\n"
                "- collision handling\n"
                "- service behavior\n\n"
                "## Integration\n"
                "- create\n- redirect\n- analytics\n- health\n"
                "- persistence\n- invalid/missing inputs\n\n"
                "## Orchestration\n"
                "- dependency resolution\n"
                "- concurrent ready tasks\n"
                "- bounded retry\n"
                "- rejection/recovery\n"
                "- approval\n\n"
                "## E2E\n"
                "- mandatory requirement through final engineering summary\n"
            ),
            "generated_code.py": generated_service,
            "generated_tests.py": generated_tests,
            "risks-and-tradeoffs.md": (
                "# Risks and Trade-offs\n\n"
                "- SQLite is demo-friendly but not a high-scale production datastore.\n"
                "- Short-code collisions use a uniqueness constraint and bounded retry.\n"
                "- Analytics are intentionally basic for the prototype.\n"
                "- Model-generated output can be wrong, so deterministic validation, "
                "tests, and human approval remain authoritative.\n"
                "- The prototype never blindly executes arbitrary generated source code.\n"
            ),
        }

        refs: list[str] = []
        for name, content in files.items():
            path = self.output_dir / name
            path.write_text(content, encoding="utf-8")
            refs.append(str(path))

        return {
            "artifacts": {
                "generated_files": refs,
                "artifact_manifest": list(files),
            }
        }
