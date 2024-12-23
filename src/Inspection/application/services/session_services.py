from Inspection.ports.input import SessionServicesPort
from Inspection.ports.ouput import SessionControllerPort

class SessionServices(SessionServicesPort):
    def __init__(self, session_controller:SessionControllerPort):
        super().__init__()
        self.session_controller = session_controller

    def begin_session(self, name:str) -> bool:
        return self.session_controller.begin_session(name=name)
    
    def take_capture(self) -> None:
        self.session_controller.take_capture()
    
    def start_recording(self) -> None:
        self.session_controller.start_recording()
    
    def stop_recording(self) -> None:
        self.session_controller.stop_recording()

    def finish_session(self) -> None:
        self.session_controller.finish_session()

    def is_new(self, name) -> bool:
        return self.session_controller.is_new(name=name)
    
    def get_sessions(self) -> list:
        return self.session_controller.get_sessions()

    def download_session(self, session_name:str, target_folder:str): 
        self.session_controller.download_session(session_name=session_name, target_folder=target_folder)
