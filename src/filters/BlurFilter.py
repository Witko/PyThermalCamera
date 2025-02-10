import cv2
from numpy import ndarray

from src.filters.Filter import Filter


class BlurFilter(Filter):

    def __init__(self):
        self.rad = 0

    def set_blur(self, rad: int):
        self.rad = rad

    def apply(self, image_data: ndarray) -> ndarray:
        if self.rad == 0:
            return image_data
        return cv2.blur(image_data, (self.rad, self.rad))
