from Inspection.ports.output.session_controller_port import SessionControllerPort
from Video.application.services.session_services import SessionServices
from Video.domain.entities.dvr_entities import DvrOrder
from logging import Logger

class VideoSessionControllerAdapter(SessionControllerPort):
    def __init__(self, control_session:SessionServices, logger:Logger) -> None:
        super().__init__()
        self.control_session = control_session
        self.logger = logger

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
    
    def get_sessions(self) -> list:
        return self.control_session.get_sessions()
    
    def download_session(self, session_name, target_folder): 
        return self.control_session.download_session(session_name, target_folder)