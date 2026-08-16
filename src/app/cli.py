import argparse
import asyncio
import json
from pathlib import Path

from app.config import get_settings
from app.orchestration.orchestrator import WorkflowOrchestrator

MANDATORY_REQUIREMENT = (
    "Build a scalable URL shortener service with APIs, persistence, and analytics."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agentic software engineering demo")
    subparsers = parser.add_subparsers(dest="command", required=True)
    demo = subparsers.add_parser("demo", help="Run the end-to-end workflow")
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
    root = Path.cwd()
    orchestrator = WorkflowOrchestrator(
        root,
        args.output_dir,
        settings.max_retries,
        settings.approval_required,
    )
    state = await orchestrator.run(
        args.requirement,
        args.mode,
        auto_approve=not args.no_auto_approve,
    )
    print(json.dumps(state.model_dump(mode="json"), indent=2))


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "demo":
        asyncio.run(run_demo(args))


if __name__ == "__main__":
    main()
