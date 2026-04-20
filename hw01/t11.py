import numpy as np

from hw01.utils import get_rectanglescene
from utils import get_rectanglescene

TRS = np.array([
    [2.934, -0.416, 2.000],
    [0.624, 1.956,  3.400],
    [0,     0,      1    ]
], dtype=np.float64)


def frame1(scene):
    vertices_h = np.array([
        [2,   3.4, 1],
        [4.9, 4,   1],
        [4.5, 6,   1],
        [1.6, 5.4, 1]], dtype=np.float64)

    rect = scene["rect"]
    rect["color"] = "blue"
    rect.set_geometry(vertices_h[:, :2].flatten())


def frame2(scene):
    vertices_h = np.array([
        [2, 3.4, 1],
        [4.9, 4, 1],
        [4.5, 6, 1],
        [1.6, 5.4, 1]], dtype=np.float64)

    TRS_inv = np.linalg.inv(TRS)
    print(TRS_inv)

    vertices_h = (TRS_inv @ vertices_h.T).T
    print(np.round(vertices_h[:, :2]))

    rect = scene["rect"]
    rect["color"] = "red"
    rect.set_geometry(vertices_h[:, :2].flatten())


if __name__ == '__main__':
    scene = get_rectanglescene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.show()

