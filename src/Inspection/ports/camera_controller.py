from abc import ABC, abstractmethod

class CameraController(ABC):
    @abstractmethod
    def tilt_up(self) -> None:
        pass

    @abstractmethod
    def tilt_down(self) -> None:
        pass

    @abstractmethod
    def tilt_stop(self) -> None:
        pass

    @abstractmethod
    def pan_left(self) -> None:
        pass

    @abstractmethod
    def pan_right(self) -> None:
        pass

    @abstractmethod
    def pan_stop(self) -> None:
        pass

    @abstractmethod
    def focus_in(self) -> None:
        pass

    @abstractmethod
    def focus_out(self) -> None:
        pass

    @abstractmethod
    def focus_stop(self) -> None:
        pass

    @abstractmethod
    def init_camera(self) -> None:
        pass

