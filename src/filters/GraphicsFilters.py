from numpy import ndarray

from src.filters.BlurFilter import BlurFilter
from src.filters.ColorMapFilter import ColorMapFilter
from src.filters.ContrastFilter import ContrastFilter
from src.filters.RotateFilter import RotateFilter
from src.filters.ScaleFilter import ScaleFilter


class GraphicsEffects:

    def __init__(self):
        self.__scale_filter = ScaleFilter()
        self.__contrast_filter = ContrastFilter()
        self.__color_map_filter = ColorMapFilter()
        self.__blur_filter = BlurFilter()
        self.__rotate_filter = RotateFilter()

    def set_scale(self, scale: float):
        self.__scale_filter.set_scale(scale)

    def set_colormap(self, colormap: int):
        self.__color_map_filter.set_color_map(colormap)

    def set_rotate(self, mode: int):
        self.__rotate_filter.set_mode(mode)

    def process(self, image_data: ndarray) -> ndarray:
        image_data = self.__contrast_filter.apply(image_data)
        # image_data = self.__scale_filter.apply(image_data)
        image_data = self.__blur_filter.apply(image_data)
        image_data = self.__color_map_filter.apply(image_data)
        image_data = self.__rotate_filter.apply(image_data)
        return image_data

    def set_blur(self, value:int):
        self.__blur_filter.set_blur(value)

    def set_contrast(self, value:int):
        self.__contrast_filter.set_alpha(value)
