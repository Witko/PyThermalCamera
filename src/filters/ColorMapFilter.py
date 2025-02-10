import cv2
from numpy import ndarray

from src.filters.Filter import Filter


class ColorMapFilter(Filter):

    def __init__(self):
        self.color_map = cv2.COLORMAP_JET

    def set_color_map(self, color_map: int):
        self.color_map = color_map

    def apply(self, image_data: ndarray) -> ndarray:
        return cv2.applyColorMap(image_data, self.color_map)
