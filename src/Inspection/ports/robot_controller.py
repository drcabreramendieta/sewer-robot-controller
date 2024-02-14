from abc import ABC, abstractmethod

class RobotController(ABC):
    @abstractmethod
    def move_forward(self) -> None:
        pass
    
    @abstractmethod
    def move_backward(self) -> None:
        pass
    
    @abstractmethod
    def rotate_left_forward(self) -> None:
        pass
    
    @abstractmethod
    def rotate_right_forward(self) -> None:
        pass

    @abstractmethod
    def rotate_left_backward(self) -> None:
        pass

    @abstractmethod
    def rotate_right_backward(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass