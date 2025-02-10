import cv2
from numpy import ndarray

from src.filters.Filter import Filter


class RotateFilter(Filter):

    def __init__(self):
        self.mode = -1

    def set_mode(self, mode: int):
        self.mode = mode

    def apply(self, image_data: ndarray) -> ndarray:
        if self.mode == -1:
            return image_data
        return cv2.rotate(image_data, self.mode)  #
