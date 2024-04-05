from Video.domain.entities import ImageInfo, RecordInfo
from abc import ABC, abstractmethod

class DbLink:
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