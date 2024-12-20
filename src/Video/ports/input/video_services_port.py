from abc import ABC, abstractmethod
from Video.ports.output.video_observer_port import VideoObserverPort

class VideoServicesPort(ABC):
    @abstractmethod
    def register_observer(self, observer:VideoObserverPort):
        pass

    @abstractmethod
    def start_listening(self):
        pass

    @abstractmethod
    def stop_listening(self):
        pass