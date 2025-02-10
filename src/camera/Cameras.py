import string
from typing import Union

import cv2

from src.camera.devices.TopdonTS001 import TopdonTS001


class Cameras():
    def __init__(self):
        # checks the first 10 indexes.
        index = 0
        arr = []
        i = 10
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        self.__cameras = arr

    def get_cameras(self):
        return map(lambda c: [c, "/dev/video" + str(c)], self.__cameras)

    def open_camera(self, camera: Union[int, string]):
        if type(camera) == int:
            return TopdonTS001().open("/dev/video/" + str(camera))
        return TopdonTS001().open(str(camera))
