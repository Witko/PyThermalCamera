from typing import Union

from PyQt6.QtCore import QPoint, QSize


class Projection:
    def __init__(self):
        self.__rotation = 0
        self.__scale = 1
        self.__source_size = (1, 1)
        self.__original_target_size = (1, 1)
        self.__target_size = (1, 1)

    def update(self, source_size: Union[tuple[int, int], QPoint], target_size: Union[tuple[int, int], QPoint, QSize]):
        self.__source_size = self.to_tuple(source_size)
        self.__original_target_size = self.to_tuple(target_size)

        if self.__rotation == 0 or self.__rotation == 180:
            self.__target_size = self.__original_target_size
        elif self.__rotation == 90 or self.__rotation == 270:
            self.__target_size = self.flip(self.__original_target_size)

        scale_x = self.__target_size[0] / self.__source_size[0]
        scale_y = self.__target_size[1] / self.__source_size[1]
        self.__scale = min(scale_x, scale_y)

    def set_rotation(self, rotation: int):
        assert rotation in [0, 90, 180, 270]
        self.__rotation = rotation
        self.update(self.__source_size, self.__original_target_size)

    def project(self, point: Union[tuple[int, int], QPoint]) -> tuple[int, int]:
        to_tuple = self.to_tuple(point)
        to_tuple = self.flip(to_tuple)
        to_tuple = self.rotate_source_point(to_tuple, angle=self.__rotation)
        to_tuple = (int(to_tuple[0] * self.__scale),
                    int(to_tuple[1] * self.__scale))
        return to_tuple

    def invert(self, point: Union[tuple[int, int], QPoint]) -> tuple[int, int]:
        to_tuple = self.to_tuple(point)
        to_tuple = int(to_tuple[0] / self.__scale), int(to_tuple[1] / self.__scale)
        to_tuple = self.rotate_target_point(to_tuple, angle=self.__rotation)
        to_tuple = self.flip(to_tuple)
        return to_tuple

    def flip(self, point: Union[tuple[int, int], QPoint]):
        t = self.to_tuple(point)
        return t[1], t[0]

    def to_tuple(self, point: Union[tuple[int, int], QPoint, QSize]) -> tuple[int, int]:
        if type(point) == QPoint:
            return point.x(), point.y()
        if type(point) == QSize:
            return point.width(), point.height()
        return point

    def rotate_source_point(self, point, angle: int):
        if angle == 0:
            return point
        assert angle in [90, 180, 270], "Angle must be one of 90, 180, 270 degrees"

        x, y = point
        if angle == 90:
            return self.__source_size[1] - y, x
        elif angle == 180:
            return self.__source_size[0] - x, self.__source_size[1] - y
        elif angle == 270:
            return y, self.__source_size[0] - x,

    def rotate_target_point(self, point, angle: int):
        if angle == 0:
            return point
        assert angle in [90, 180, 270], "Angle must be one of 90, 180, 270 degrees"

        x, y = point
        if angle == 90:
            return y, self.__source_size[1] - x
        elif angle == 180:
            return self.__source_size[0] - x, self.__source_size[1] - y
        elif angle == 270:
            return self.__source_size[0] - y,  x,
