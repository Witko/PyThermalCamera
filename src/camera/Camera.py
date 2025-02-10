from abc import ABC, abstractmethod

from src.camera.ThermalFrame import ThermalFrame


class Camera(ABC):
    @abstractmethod
    def open(self, path_to_device):
        pass

    @abstractmethod
    def get_capture_size(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def capture_frame(self) -> ThermalFrame:
        pass

    @abstractmethod
    def get_fps(self) -> int:
        pass

    @abstractmethod
    def close(self):
        pass
