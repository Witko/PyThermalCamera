from src.Projection import Projection


def test_project():
    projection = Projection()
    projection.update((20, 10), (40, 30))
    projected = projection.project((20, 10))
    assert projected == (20, 40)
    assert projection.invert((20, 40)) == (20, 10)


def test_rotate_point_90():
    projection = Projection()
    projection.update((10, 20), (1, 1))
    rotated = projection.rotate_source_point((6, 7), 90)
    assert rotated == (13, 6)


def test_rotate_point_90_2():
    projection = Projection()
    projection.update((20, 10), (1, 1))
    rotated = projection.rotate_source_point((6, 7), 90)
    assert rotated == (3, 6)


def test_rotate_point_180():
    projection = Projection()
    projection.update((10, 20), (1, 1))
    rotated = projection.rotate_source_point((6, 7), 180)
    assert rotated == (4, 13)


def test_rotate_point_270():
    projection = Projection()
    projection.update((10, 20), (1, 1))
    rotated = projection.rotate_source_point((6, 7), 270)
    assert rotated == (7, 4)

def test_rotate_point_0_project():
    projection = Projection()
    projection.set_rotation(90)
    projection.update((256, 192), (513, 567))
    rotated = projection.project((71, 90))
    assert rotated == (267, 199)
    assert projection.invert((267, 199)) == (72, 89)


def test_rotate_point_90_project():
    projection = Projection()
    projection.set_rotation(90)
    projection.update((256, 192), (512, 686))
    rotated = projection.project((49, 159))
    assert rotated == (381, 424)
