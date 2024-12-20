from Video.ports.input import VideoServicesPort
from Video.ports.output.video_observer_port import VideoObserverPort
from Video.domain.entities.video_entities import VideoMessage
from Video.ports.output.video_controller_port import VideoControllerPort
from logging import Logger

class VideoServices(VideoServicesPort):
    def __init__(self, link:VideoControllerPort, logger:Logger, video_observers:list[VideoObserverPort]|None=None) -> None:
        self.video_observers = video_observers if video_observers else []
        self.link = link
        self.logger = logger
        link.callback_setup(self._notify)

    def _notify(self, video:VideoMessage) -> None:
        for observer in self.video_observers:
            observer.on_video_ready(video=video)

    def register_observer(self, observer:VideoObserverPort):
        self.video_observers.append(observer)

    def start_listening(self):
        print('start')
        self.link.start_listening()

    def stop_listening(self):
        self.link.stop_listening()