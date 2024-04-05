from Video.ports.dvr_link import DvrLink
from Video.domain.entities import Session
from Video.domain.entities import DvrOrder

class ControlSession:
    def __init__(self, dvr_link:DvrLink) -> None:
        self.dvr_link = dvr_link
        self.session = None

    def create_session(self, name:str) -> Session:
        self.session = Session(name=name, captures=[], records=[], recording=False)

    def run(self, order:DvrOrder):
        if self.session:
            if order == DvrOrder.TAKE_PHOTO:
                self.session.captures.append(self.dvr_link.take_image())
            elif order == DvrOrder.START_RECORDING:
                self.session.recording = self.dvr_link.start_recording()
            elif order == DvrOrder.STOP_RECORDING and self.session.recording:
                self.session.records.append(self.dvr_link.stop_recording())
            print(self.session)