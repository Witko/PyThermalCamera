from abc import ABC, abstractmethod

from numpy import ndarray


class Filter(ABC):
    @abstractmethod
    def apply(self, image_data: ndarray) -> ndarray:
        pass
