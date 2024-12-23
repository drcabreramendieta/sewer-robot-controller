from abc import ABC, abstractmethod

class SessionControllerPort(ABC):
    @abstractmethod
    def begin_session(self, name:str) -> bool:
        pass
    
    @abstractmethod
    def take_capture(self) -> None:
        pass
    
    @abstractmethod
    def start_recording(self) -> None:
        pass
    
    @abstractmethod
    def stop_recording(self) -> None:
        pass

    @abstractmethod
    def finish_session(self) -> None:
        pass

    @abstractmethod
    def is_new(self, name) -> bool:
        pass
    
    @abstractmethod
    def get_sessions(self) -> list:
        pass
    
    @abstractmethod
    def download_session(self, session_name:str, target_folder:str): 
        pass
