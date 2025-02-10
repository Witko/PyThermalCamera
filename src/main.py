from __future__ import annotations

import sys
from typing import Union, List

import cv2
from PyQt6 import QtWidgets
from PyQt6.QtCore import QPoint, QTimer, Qt
from PyQt6.QtGui import QPainter, QImage, QPixmap, QPen, QMouseEvent
from PyQt6.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QLabel

from src.Projection import Projection
from src.camera.Cameras import Cameras
from src.filters.GraphicsFilters import GraphicsEffects


class PyThermalCameraWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self._effects = GraphicsEffects()
        self.cameras = Cameras()
        self.camera = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update_image)
        self.__projection = Projection()
        self.setupUi(self)

        self._custom_measurements: List[tuple[int, int]] = []
        self._effects.set_scale(2)
        QTimer.singleShot(100, self.recalculate_projection)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.setWindowTitle("PyThermalCamera")

        main_panel = QtWidgets.QHBoxLayout()
        side_panel = QtWidgets.QVBoxLayout()

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_panel)
        self.setCentralWidget(central_widget)

        self.canvas = QGraphicsScene()
        self.view = QGraphicsView(self.canvas)

        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_panel.addWidget(self.view)

        camera_combo = QtWidgets.QComboBox()
        camera_combo.setObjectName("cameraCombo")
        camera_combo.currentTextChanged.connect(lambda text: self.on_camera_selected(text))
        for c in self.cameras.get_cameras():
            camera_combo.addItem(c[1])

        color_mode_combo = QtWidgets.QComboBox()
        color_mode_combo.setObjectName("colorModeCombo")
        color_mode_combo.currentIndexChanged.connect(lambda index: self._effects.set_colormap(color_mode_combo.itemData(index)))
        cv_dict = cv2.__dict__
        color_maps = {k: v for (k, v) in cv_dict.items() if "COLORMAP" in k}
        for cm in color_maps:
            color_mode_combo.addItem(cm, cv_dict[cm])

        rotations = {
            "No Rotation": -1,
            "90 Clockwise": cv2.ROTATE_90_CLOCKWISE,
            "180": cv2.ROTATE_180,
            "90 Counterclockwise": cv2.ROTATE_90_COUNTERCLOCKWISE,

        }
        rotation_combo = QtWidgets.QComboBox()
        rotation_combo.setObjectName("rotationModeCombo")
        rotation_combo.currentIndexChanged.connect(lambda index: self.on_rotate(rotation_combo.itemData(index)))
        for c in rotations:
            rotation_combo.addItem(c, rotations[c])

        blur_slider = QtWidgets.QSlider()
        blur_slider.setObjectName("blurSlider")
        blur_slider.setMinimum(0)
        blur_slider.setMaximum(5)
        blur_slider.setOrientation(Qt.Orientation.Horizontal)
        blur_slider.valueChanged.connect(lambda value: self._effects.set_blur(value))

        contrast_slider = QtWidgets.QSlider()
        contrast_slider.setObjectName("contrastSlider")
        contrast_slider.setMinimum(1)
        contrast_slider.setMaximum(20)
        contrast_slider.setValue(10)
        contrast_slider.setOrientation(Qt.Orientation.Horizontal)
        contrast_slider.valueChanged.connect(lambda value: self._effects.set_contrast(value/10))

        side_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        side_panel.addWidget(QLabel("Capture device"))
        side_panel.addWidget(camera_combo)
        side_panel.addWidget(QLabel("Colorspace"))
        side_panel.addWidget(color_mode_combo)
        side_panel.addWidget(QLabel("Rotation"))
        side_panel.addWidget(rotation_combo)
        side_panel.addWidget(QLabel("Blur"))
        side_panel.addWidget(blur_slider)
        side_panel.addWidget(QLabel("Contrast"))
        side_panel.addWidget(contrast_slider)

        main_panel.addWidget(self.view)
        side_widget = QtWidgets.QWidget()
        side_widget.setMaximumWidth(200)
        side_widget.setLayout(side_panel)
        main_panel.addWidget(side_widget)

    def on_camera_selected(self, device_path):
        if self._timer:
            self._timer.stop()
        if self.camera:
            self.camera.close()

        if device_path == None:
            return

        try:
            self.camera = self.cameras.open_camera(device_path)
            self.recalculate_projection()
            self._timer.start(int(1000 / self.camera.get_fps()))

        except Exception as e:
            print("Error" + str(e))
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Oh no!')
            error_dialog.show()

    def resizeEvent(self, event):
        self.recalculate_projection()

    def recalculate_projection(self):
        self.__projection.update(self.camera.get_capture_size(), self.view.size())

    def mousePressEvent(self, event: QMouseEvent):
        if self.view.underMouse():
            if event.button() == Qt.MouseButton.LeftButton:
                point = event.pos()
                point = self.view.mapFromGlobal(point)
                pointf = self.view.mapToScene(point)
                inverted = self.__projection.invert((int(pointf.x()), int(pointf.y())))
                self._custom_measurements.append((max(0, inverted[0]), max(0, inverted[1])))
        if event.button() == Qt.MouseButton.RightButton:
            self._custom_measurements.clear()

    def on_rotate(self, rotation: int):
        self._effects.set_rotate(rotation)
        match rotation:
            case -1:
                self.__projection.set_rotation(0)
            case cv2.ROTATE_90_CLOCKWISE:
                self.__projection.set_rotation(90)
            case cv2.ROTATE_180:
                self.__projection.set_rotation(180)
            case cv2.ROTATE_90_COUNTERCLOCKWISE:
                self.__projection.set_rotation(270)

    def update_image(self):
        self.canvas.clear()
        if self.camera == None:
            return

        frame = self.camera.capture_frame()
        image = self._effects.process(frame.image_data())

        q_img = QImage(image, image.shape[1], image.shape[0], QImage.Format.Format_BGR888)
        q_img = q_img.scaled(self.view.viewport().width(),
                             self.view.viewport().height(),
                             Qt.AspectRatioMode.KeepAspectRatio,
                             Qt.TransformationMode.SmoothTransformation)

        q_painter = QPainter(q_img)
        self.draw_crosshair_with_temp(q_painter, frame.temperatureAt(frame.midpoint()), (int(q_img.width() / 2), int(q_img.height() / 2)))

        coldspot = frame.coldspot()
        self.draw_crosshair_with_temp(q_painter,
                                      frame.temperatureAt(coldspot),
                                      self.__projection.project(coldspot))

        hotspot = frame.hotspot()
        self.draw_crosshair_with_temp(q_painter,
                                      frame.temperatureAt(hotspot),
                                      self.__projection.project(hotspot))

        for m in self._custom_measurements:
            x, y = self.__projection.project(m)
            pos = max(0, min(x, q_img.width())), max(0, min(y, q_img.height()))
            temp_pos = min(m[0], frame.height() - 1), min(m[1], frame.width() - 1)
            self.draw_crosshair_with_temp(q_painter, frame.temperatureAt(temp_pos), pos)

        q_painter.end()
        self.canvas.addPixmap(QPixmap.fromImage(q_img, )).setPos(6, 6)

    def draw_crosshair_with_temp(self, painter: QPainter, temp: float, point: Union[tuple[int, int], QPoint]):
        x, y = self.__projection.to_tuple(point)
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.drawLine(x - 10, y, x + 10, y)
        painter.drawLine(x, y - 10, x, y + 10)
        painter.drawText(x + 4, y + 14, str(temp))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = PyThermalCameraWindow()
    clock.show()
    sys.exit(app.exec())
