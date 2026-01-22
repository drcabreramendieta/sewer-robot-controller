from abc import ABC, abstractmethod

class FeederControllerPort(ABC):

    @abstractmethod
    def send_message(self, msg:str) -> None:
        pass