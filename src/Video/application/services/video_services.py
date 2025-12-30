from Video.ports.input import VideoServicesPort
from Video.ports.output.video_observer_port import VideoObserverPort
from Video.domain.entities.video_entities import VideoMessage
from Video.ports.output.video_controller_port import VideoControllerPort
from logging import Logger
from typing import List

class VideoServices(VideoServicesPort):
    observers:List[VideoObserverPort]
    def __init__(self, video_controller:VideoControllerPort, logger:Logger, observer:VideoObserverPort) -> None:
        super().__init__()
        self.observers = []
        self.observer = observer
        if self.observer:
            self.observers.append(self.observer)
        self.video_controller = video_controller
        self.logger = logger
        video_controller.callback_setup(self._notify)

    def _notify(self, video:VideoMessage) -> None:
        for observer in self.observers:
            observer.on_video_ready(video=video)

    def register_observer(self, observer:VideoObserverPort):
        self.observers.append(observer)

    def start_listening(self):
        print('start')
        self.video_controller.start_listening()

    def stop_listening(self):
        self.video_controller.stop_listening()
