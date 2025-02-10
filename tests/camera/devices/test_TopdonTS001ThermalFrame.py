from numpy import array

from src.camera.devices.TopdonTS001ThermalFrame import TopdonTS001ThermalFrame

image_data = array(
    [
        [[0, 1, 2], [0, 1, 2], [0, 1, 2]],
        [[0, 1, 2], [0, 1, 2], [0, 1, 2]],
        [[0, 1, 2], [0, 1, 2], [0, 1, 2]],
        [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
    ])
thermal_data = array(
    [
        [[1, 8], [5, 50], [4, 65]],
        [[4, 5], [2, 7], [150, 200]],
        [[240, 10], [151, 200], [45, 80]],
        [[4, 10], [2, 5], [45, 5]]
    ])

frame = TopdonTS001ThermalFrame(image_data, thermal_data)


def test_width():
    assert frame.width() == 3


def test_height():
    assert frame.height() == 4


def test_temperature_at():
    assert frame.temperatureAt((2,2))== 47.55


def test_midpoint():
    assert frame.midpoint()== (2,1)


def test_hotspot():
    assert frame.hotspot()== (2,1)


def test_coldspot():
    assert frame.coldspot()== (3,1)
