from abc import ABC, abstractmethod

from numpy import ndarray


class ThermalFrame(ABC):

    @abstractmethod
    def image_data(self) -> ndarray:
        pass

    @abstractmethod
    def width(self):
        pass

    @abstractmethod
    def height(self):
        pass

    @abstractmethod
    def temperatureAt(self, point: (int, int)):
        pass

    @abstractmethod
    def midpoint(self) -> (int, int):
        pass

    @abstractmethod
    def hotspot(self) -> (int, int):
        pass

    @abstractmethod
    def coldspot(self) -> (int, int):
        pass
