import cv2
from numpy import ndarray

from src.filters.Filter import Filter


class ScaleFilter(Filter):

    def __init__(self):
        self.scale = 1

    def set_scale(self, scale: float):
        self.scale = scale

    def apply(self, image_data: ndarray) -> ndarray:
        if self.scale == 1:
            return image_data
        return cv2.resize(image_data,
                          (int(image_data.shape[0] * self.scale), int(image_data.shape[1] * self.scale)),
                          interpolation=cv2.INTER_CUBIC)  #
