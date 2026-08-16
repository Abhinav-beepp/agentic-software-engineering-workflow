from pathlib import Path

import pytest

from app.agents.brownfield import BrownfieldAgent
from app.models import WorkflowState


@pytest.mark.asyncio
async def test_brownfield_scanner_only_reports_observed_files(
    tmp_path: Path,
) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "service.py").write_text("class Service: pass")
    state = WorkflowState(requirement="Add rate limiting")
    result = await BrownfieldAgent(tmp_path).execute(state)
    analysis = result["brownfield_analysis"]
    assert analysis["file_count"] == 1
    assert "src/service.py" in analysis["relevant_files"]
