from Inspection.ports.session_controller import SessionController
from Video.domain.use_cases.control_session import ControlSession
from Video.domain.entities import DvrOrder

class GidtecSessionController(SessionController):
    def __init__(self, control_session:ControlSession) -> None:
        super().__init__()
        self.control_session = control_session

    def begin_session(self, name:str) -> bool:
        return self.control_session.create_session(name)
    
    def take_capture(self) -> None:
        print('take capture')
        self.control_session.run(DvrOrder.TAKE_PHOTO)
    
    def start_recording(self) -> None:
        print('start recording')
        self.control_session.run(DvrOrder.START_RECORDING)
    
    def stop_recording(self) -> None:
        print('stop recording')
        self.control_session.run(DvrOrder.STOP_RECORDING)

    def finish_session(self) -> None:
        print('No implementado')

    def is_new(self, name) -> bool:
        return not self.control_session.name_exists(name)