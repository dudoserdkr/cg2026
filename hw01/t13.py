import numpy as np

from utils import decompose_trs, get_vertices, get_homogeneous_vertices, get_rectanglescene


TRS = np.array([
    [1.414,  -2.121,  1],
    [1.414,  2.121,   1],
    [0,      0,       1]
], dtype=np.float64)


def frame1(scene):
    rect_vertices = get_vertices()
    rect = scene["rect"]
    rect["color"] = "blue"
    rect.set_geometry(rect_vertices.flatten())


def frame2(scene):
    vertices_h = get_homogeneous_vertices()
    vertices_h = (TRS @ vertices_h.T).T

    rect = scene["rect"]
    rect["color"] = "red"
    rect.set_geometry(vertices_h[:, :2].flatten())


if __name__ == '__main__':
    R, T, S = decompose_trs(TRS)
    print(R)
    print()
    print(T)
    print(S)
    print()
    scene = get_rectanglescene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.show()
