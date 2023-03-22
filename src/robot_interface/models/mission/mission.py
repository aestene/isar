from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4

from isar.services.utilities.uuid_string_factory import uuid4_string
from robot_interface.models.mission.status import MissionStatus
from robot_interface.models.mission.task import Task


@dataclass
class Mission:
    tasks: List[Task]
    id: str = field(default_factory=uuid4_string, init=True)
    status: MissionStatus = MissionStatus.NotStarted

    def _set_unique_id(self) -> None:
        self.id: UUID = uuid4()

    def __post_init__(self) -> None:
        if self.id is None:
            self._set_unique_id()
