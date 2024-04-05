from abc import ABC, abstractmethod

class SessionController(ABC):
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
