import numpy as np

from utils import decompose_trs, get_vertices, get_homogeneous_vertices, get_rectanglescene


TRS = np.array([
    [0.866, 0.5,   4],
    [0.5,   0.866, 3],
    [0,     0,     1]
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
    # R, T, S = decompose_trs(TRS) # We can't decompose TRS because there is no rotation matrix there
    scene = get_rectanglescene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.show()
