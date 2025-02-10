import cv2
from numpy import ndarray

from src.filters.Filter import Filter


class ContrastFilter(Filter):

    def __init__(self):
        self.alpha = 1

    def set_alpha(self, alpha: int):
        self.alpha = alpha

    def apply(self, image_data: ndarray) -> ndarray:
        return cv2.convertScaleAbs(image_data, alpha=self.alpha)  # Contrast
