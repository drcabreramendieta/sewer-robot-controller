from datetime import datetime
import os
from logging import Logger

from Video.domain.entities.repository_entities import ImageInfo, RecordInfo
from Video.ports.output.dvr_controller_port import DvrControllerPort


class MockHikvisionDvrControllerAdapter(DvrControllerPort):
    def __init__(self, url: str, user: str, password: str, dir: str, logger: Logger) -> None:
        super().__init__()
        self.url = url
        self.username = user
        self.password = password
        self.dir = dir
        self.logger = logger
        self.folder = None
        self.storage = dir
        self.start_time = None
        os.makedirs(self.dir, exist_ok=True)

    def take_image(self) -> ImageInfo:
        if not self.folder:
            self.logger.info("Mock take_image called without active folder.")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_name = f"image_{timestamp}.jpg"
        image_path = os.path.join(self.storage, image_name)
        with open(image_path, "wb") as image_file:
            image_file.write(b"")
        return ImageInfo(image_path, timestamp)

    def download_video(self, session_info, target_folder):
        records = session_info.get("records", [])
        if not records:
            return True
        os.makedirs(target_folder, exist_ok=True)
        for record in records:
            record_path = record.get("path")
            if not record_path:
                continue
            filename = os.path.basename(record_path)
            destination = os.path.join(target_folder, filename)
            if os.path.exists(record_path):
                with open(record_path, "rb") as source_file, open(destination, "wb") as dest_file:
                    dest_file.write(source_file.read())
        return True

    def search_video(self, session_info):
        records = session_info.get("records", [])
        if not records:
            return [], True
        uris = [record.get("path") for record in records if record.get("path")]
        return uris, True

    def start_recording(self) -> bool:
        self.start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        return True

    def stop_recording(self) -> RecordInfo:
        end_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not self.start_time:
            self.start_time = end_time
        record_name = f"record_{self.start_time}_{end_time}.mp4"
        record_path = os.path.join(self.storage, record_name)
        with open(record_path, "wb") as record_file:
            record_file.write(b"")
        return RecordInfo(record_path, end_time, self.start_time)

    def set_folder(self, name: str) -> None:
        self.folder = name
        self.storage = os.path.join(self.dir, self.folder)
        os.makedirs(self.storage, exist_ok=True)
