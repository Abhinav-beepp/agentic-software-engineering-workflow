from pathlib import Path

from app.models import ValidationResult, WorkflowState


class EngineeringValidator:
    REQUIRED_TASKS = {
        "analysis",
        "architecture",
        "api",
        "database",
        "implementation",
        "tests",
        "risks",
        "validation",
        "approval",
        "summary",
    }

    def validate(
        self,
        state: WorkflowState,
        project_root: Path,
    ) -> ValidationResult:
        checks: list[str] = []
        failures: list[str] = []
        warnings: list[str] = []
        required_tasks = set(self.REQUIRED_TASKS)
        if state.mode == "brownfield":
            required_tasks.add("brownfield_scan")

        missing = required_tasks - set(state.tasks)
        if missing:
            failures.append(f"Missing required tasks: {sorted(missing)}")
        else:
            checks.append("All required workflow tasks exist")

        if state.analysis and state.analysis.acceptance_criteria:
            checks.append("Requirement analysis contains acceptance criteria")
        else:
            failures.append("Requirement analysis lacks acceptance criteria")

        if state.architecture and state.architecture.components:
            checks.append("Architecture contains components")
        else:
            failures.append("Architecture is missing")

        generated_files = state.artifacts.get("generated_files", [])
        if generated_files:
            checks.append("Engineering artifact files were generated")
            for raw in generated_files:
                if not Path(raw).exists():
                    failures.append(f"Missing generated artifact: {raw}")
        else:
            failures.append("No generated artifact files found")

        if state.artifacts.get("api_contract"):
            checks.append("API contract exists")
        else:
            failures.append("API contract missing")

        if state.artifacts.get("test_plan"):
            checks.append("Test plan exists")
        else:
            failures.append("Test plan missing")

        manifest = set(state.artifacts.get("artifact_manifest", []))
        required_artifacts = {
            "implementation_plan.md",
            "architecture.md",
            "api_contract.json",
            "database_schema.md",
            "test_plan.md",
            "generated_code.py",
            "generated_tests.py",
            "risks-and-tradeoffs.md",
        }
        missing_artifacts = required_artifacts - manifest
        if missing_artifacts:
            failures.append(f"Generated artifact manifest missing: {sorted(missing_artifacts)}")
        else:
            checks.append("Code and test generation artifacts are present in the manifest")

        app_file = project_root / "src" / "app" / "main.py"
        if app_file.exists():
            checks.append("Runnable application entrypoint exists")
        else:
            failures.append("Application entrypoint missing")

        warnings.append(
            "Prototype validation does not execute generated arbitrary code; "
            "it relies on the repository test suite and deterministic artifact checks."
        )
        return ValidationResult(
            passed=not failures,
            checks=checks,
            failures=failures,
            warnings=warnings,
        )
