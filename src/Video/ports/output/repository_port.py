from Video.domain.entities.repository_entities import ImageInfo
from Video.domain.entities.repository_entities import RecordInfo
from abc import ABC, abstractmethod

class RepositoryPort(ABC):
    @abstractmethod
    def create(self, name:str) -> bool:
        pass
    
    @abstractmethod
    def add_capture(self, capture:ImageInfo):
        pass

    @abstractmethod
    def add_record(self, record:RecordInfo):
        pass
    
    @abstractmethod
    def update_status(self, recording:bool):
        pass
    
    @abstractmethod
    def get_status(self):
        pass
    
    @abstractmethod
    def session_exists(self, name):
        pass

    @abstractmethod
    def print_session(self):
        pass
    
    @abstractmethod
    def print_all_sessions(self):
        pass
    
    @abstractmethod
    def get_session(self, name:str)->dict:
        pass

    @abstractmethod
    def get_sessions(self):
        pass

    @abstractmethod
    def is_session_attached(self):
        pass