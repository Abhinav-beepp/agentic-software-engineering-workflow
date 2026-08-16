from abc import ABC, abstractmethod
from typing import Any

from app.models import WorkflowState


class Agent(ABC):
    name: str

    @abstractmethod
    async def execute(self, state: WorkflowState) -> dict[str, Any]:
        raise NotImplementedError
