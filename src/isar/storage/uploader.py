import logging
from queue import Empty, Queue
from typing import List

from isar.models.mission_metadata.mission_metadata import MissionMetadata
from isar.storage.storage_interface import StorageException, StorageInterface
from robot_interface.models.inspection.inspection import Inspection


class Uploader:
    def __init__(
        self, upload_queue: Queue, storage_handlers: List[StorageInterface]
    ) -> None:
        self.upload_queue: Queue = upload_queue
        self.storage_handlers: List[StorageInterface] = storage_handlers

        self.logger = logging.getLogger("uploader")

    def run(self) -> None:
        while True:
            inspection: Inspection
            mission_metadata: MissionMetadata
            try:
                inspection, mission_metadata = self.upload_queue.get(timeout=5)
            except Empty:
                continue

            for storage_handler in self.storage_handlers:
                try:
                    storage_handler.store(
                        inspection=inspection, metadata=mission_metadata
                    )
                except StorageException:
                    self.logger.warning(
                        f"{type(storage_handler)} failed to upload inspection: {inspection.id}"
                    )