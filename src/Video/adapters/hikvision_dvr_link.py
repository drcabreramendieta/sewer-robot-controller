from Video.ports.dvr_link import DvrLink
from Video.domain.entities import ImageInfo, RecordInfo

class HikvisionDvrLink(DvrLink):
    def __init__(self) -> None:
        super().__init__()

    def take_image(self) -> ImageInfo:
        return ImageInfo('image/dvr/test', '2345')

    def download_image(self, image_info:ImageInfo) -> str:
        return image_info.path

    def download_video(self, record_info:RecordInfo) -> str:
        return record_info.path

    def start_recording(self) -> bool:
        return True

    def stop_recording(self) -> RecordInfo:
        return RecordInfo('video/dvr/test', '1234', 2)