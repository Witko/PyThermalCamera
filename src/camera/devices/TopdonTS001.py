import cv2
import numpy

from src.camera.Camera import Camera
from src.camera.ThermalFrame import ThermalFrame
from src.camera.devices.TopdonTS001ThermalFrame import TopdonTS001ThermalFrame


class TopdonTS001(Camera):

    def __init__(self):
        self.capture = None
        self.width = None
        self.height = None

    def open(self, path_to_device) -> Camera:
        self.capture = cv2.VideoCapture(path_to_device, cv2.CAP_V4L)
        self.capture.set(cv2.CAP_PROP_CONVERT_RGB, 0)
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return self

    def get_capture_size(self) -> tuple[int, int]:
        return self.width, int(self.height / 2)

    def capture_frame(self) -> ThermalFrame:
        if self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                frame = frame.reshape(self.height, self.width, 2)
                image_data, thermal_data = numpy.array_split(frame, 2)
                image_data = cv2.cvtColor(image_data, cv2.COLOR_YUV2BGR_YUYV)
                return TopdonTS001ThermalFrame(image_data=image_data, thermal_data=thermal_data)
        raise NotImplementedError

    def get_fps(self) -> int:
        return 25

    def close(self):
        self.capture.release()
        pass

    def __del__(self):
        self.close()
