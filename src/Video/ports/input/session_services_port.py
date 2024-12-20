from abc import ABC, abstractmethod
from Video.domain.entities.dvr_entities import DvrOrder

class SessionServicesPort(ABC):
    @abstractmethod
    def create_session(self, name: str) -> bool:
        pass

    @abstractmethod
    def name_exists(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_sessions(self) -> list:
        pass

    @abstractmethod
    def download_session(self, session_name, target_folder):
        pass

    @abstractmethod
    def run(self, order: DvrOrder):
        pass
