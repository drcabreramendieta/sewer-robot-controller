from Video.ports.video_observer import VideoObserver
from Video.domain.entities import VideoMessage
from Video.ports.video_link import VideoLink

class VideoNotifier:
    def __init__(self, link:VideoLink, video_observers:list[VideoObserver]|None=None) -> None:
        self.video_observers = video_observers if video_observers else []
        self.link = link
        link.callback_setup(self._notify)

    def _notify(self, video:VideoMessage) -> None:
        for observer in self.video_observers:
            observer.on_video_ready(video=video)

    def register_observer(self, observer:VideoObserver):
        self.video_observers.append(observer)

    def start_listening(self):
        print('start')
        self.link.start_listening()

    def stop_listening(self):
        self.link.stop_listening()