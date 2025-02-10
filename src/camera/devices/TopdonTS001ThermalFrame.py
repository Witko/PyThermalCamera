import numpy
from numpy import ndarray, array

from src.camera.ThermalFrame import ThermalFrame


class TopdonTS001ThermalFrame(ThermalFrame):
    def __init__(self, image_data: ndarray, thermal_data: ndarray):
        self.__image_data = image_data
        self.__thermal_data = thermal_data

    def image_data(self) -> ndarray:
        return self.__image_data

    def width(self):
        return self.__image_data.shape[1]

    def height(self):
        return self.__image_data.shape[0]

    def temperatureAt(self, point: (int, int)):
        return self.__compute_temperature_for_pixel(self.__thermal_data[point[0]][point[1]])

    def midpoint(self) -> (int, int):
        return int(self.__thermal_data.shape[0] / 2), int(self.__thermal_data.shape[1] / 2)

    def hotspot(self) -> (int, int):
        thermal_data = self.__thermal_data
        # Extracting lower and higher values
        lo_values = thermal_data[:, :, 1]
        hi_values = thermal_data[:, :, 0]

        # Finding the maximum lower value index
        max_lo_index = numpy.unravel_index(numpy.argmax(lo_values), lo_values.shape)
        max_lo_value = lo_values[max_lo_index]

        # Filtering positions with the maximum lower value
        max_lo_positions = numpy.where(lo_values == max_lo_value)

        # Extracting the corresponding higher values
        corresponding_hi_values = hi_values[max_lo_positions]

        # Finding the position with the maximum higher value
        max_hi_index = numpy.argmax(corresponding_hi_values)
        final_index = (max_lo_positions[0][max_hi_index], max_lo_positions[1][max_hi_index])

        return final_index


    def coldspot(self) -> (int, int):
        thermal_data = self.__thermal_data
        # Extracting lower and higher values
        lo_values = thermal_data[:, :, 1]
        hi_values = thermal_data[:, :, 0]

        # Finding the minimum lower value index
        min_lo_index = numpy.unravel_index(numpy.argmin(lo_values), lo_values.shape)
        min_lo_value = lo_values[min_lo_index]

        # Filtering positions with the minimum lower value
        min_lo_positions = numpy.where(lo_values == min_lo_value)

        # Extracting the corresponding higher values
        corresponding_hi_values = hi_values[min_lo_positions]

        # Finding the position with the minimum higher value
        min_hi_index = numpy.argmin(corresponding_hi_values)
        final_index = (min_lo_positions[0][min_hi_index], min_lo_positions[1][min_hi_index])

        return final_index

    def __compute_temperature_for_pixel(self, hi_lo: array):
        return self.__compute_temperature_for_pixel_(hi_lo[0], hi_lo[1])

    def __compute_temperature_for_pixel_(self, hi: numpy.uint8, lo: numpy.uint8):
        loT = 256 * int(lo)
        rawtemp = int(hi) + int(loT)
        temp = (rawtemp / 64) - 273.15
        return round(temp, 2)
