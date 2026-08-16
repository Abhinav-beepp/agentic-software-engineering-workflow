import argparse
import asyncio
import json
from pathlib import Path

from app.config import get_settings
from app.models import ApprovalDecision, TaskStatus
from app.orchestration.orchestrator import WorkflowOrchestrator


MANDATORY_REQUIREMENT = (
    "Build a scalable URL shortener service with APIs, persistence, and analytics."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Agentic software engineering demo"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    demo = subparsers.add_parser(
        "demo",
        help="Run the end-to-end workflow",
    )

    demo.add_argument(
        "--requirement",
        default=MANDATORY_REQUIREMENT,
        help="Software requirement to process",
    )

    demo.add_argument(
        "--mode",
        choices=["greenfield", "brownfield", "ambiguous"],
        default="greenfield",
    )

    demo.add_argument(
        "--output-dir",
        type=Path,
        default=Path("demo-output"),
    )

    demo.add_argument(
        "--no-auto-approve",
        action="store_true",
        help="Pause before finalization for human approval",
    )

    return parser


async def run_demo(args: argparse.Namespace) -> None:
    settings = get_settings()

    root = Path(__file__).resolve().parents[2]

    orchestrator = WorkflowOrchestrator(
        root,
        args.output_dir,
        settings.max_retries,
        settings.approval_required,
    )

    print()
    print("=" * 72)
    print("AGENTIC SOFTWARE ENGINEERING WORKFLOW")
    print("=" * 72)
    print()
    print(f"Requirement: {args.requirement}")
    print(f"Mode: {args.mode}")
    print()

    print("Running engineering workflow...")
    print()

    state = await orchestrator.run(
        args.requirement,
        args.mode,
        auto_approve=not args.no_auto_approve,
    )

    if state.tasks["approval"].status == TaskStatus.REQUIRES_APPROVAL:
        print()
        print("=" * 72)
        print("HUMAN APPROVAL REQUIRED")
        print("=" * 72)
        print()
        print(f"Workflow ID: {state.workflow_id}")
        print()
        print("Validation has completed successfully.")
        print("The engineering output is ready for human review.")
        print()

        while True:
            decision = input(
                "Approve this engineering output? [y/n]: "
            ).strip().lower()

            if decision in {"y", "yes"}:
                state = await orchestrator.approve_and_finalize(
                    state,
                    ApprovalDecision.APPROVED,
                )
                break

            if decision in {"n", "no"}:
                state = await orchestrator.approve_and_finalize(
                    state,
                    ApprovalDecision.REJECTED,
                )
                break

            print("Please enter 'y' to approve or 'n' to reject.")

    print()
    print("=" * 72)
    print("WORKFLOW COMPLETE")
    print("=" * 72)
    print()
    print(f"Workflow ID: {state.workflow_id}")
    print(f"Approval: {state.approval}")
    print(f"Validation passed: {state.validation.passed if state.validation else False}")
    print(f"Completed at: {state.completed_at}")
    print()

    if state.artifacts:
        print("Generated artifacts:")
        for artifact_name in sorted(state.artifacts):
            print(f"  - {artifact_name}")

    print()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    state_file = args.output_dir / "workflow_state.json"

    state_file.write_text(
        json.dumps(
            state.model_dump(mode="json"),
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Workflow state written to: {state_file}")
    print()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "demo":
        asyncio.run(run_demo(args))


if __name__ == "__main__":
    main()