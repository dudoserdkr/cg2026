import numpy as np
from utils import (
    get_vertices,
    get_rectanglescene,
    get_homogeneous_vertices,
    get_scale,
    get_translation,
    get_rotation_matrix,
    print_current_transformation,
)


FILE_NAME = "assets/t06.md"


def frame1(scene):
    rect_vertices = get_vertices()
    rect = scene["rect"]
    rect["color"] = "blue"
    rect.set_geometry(rect_vertices.flatten())
    print_current_transformation(vertices=rect_vertices, frame_number=1, step_number=1, file_name=FILE_NAME)


def frame2(scene):
    vertices_h = get_homogeneous_vertices() # vertices_h stands for homogeneous vertices

    S = get_scale(1, 3)
    vertices_h = (S @ vertices_h.T).T
    print_current_transformation(S=S, vertices=vertices_h, step_number=1, frame_number=2, file_name=FILE_NAME)

    R = get_rotation_matrix(60)
    vertices_h = (R @ vertices_h.T).T
    print_current_transformation(R=R, S=S, vertices=vertices_h, step_number=2, frame_number=2, file_name=FILE_NAME)

    T = get_scale(2, 3)
    vertices_h = (T @ vertices_h.T).T
    print_current_transformation(R=R, T=T, S=S, vertices=vertices_h, step_number=3, frame_number=2, file_name=FILE_NAME)

    rect = scene["rect"]
    rect.set_geometry(vertices_h[:, :2].flatten())
    rect["color"] = "red"


def frame3(scene):
    vertices_h = get_homogeneous_vertices()  # vertices_h stands for homogeneous vertices
    R = S = T = np.eye(3, dtype=np.float64)

    T = get_translation(2, 3)
    vertices_h = (T @ vertices_h.T).T
    print_current_transformation(R=R, T=T, S=S, vertices=vertices_h, step_number=1, frame_number=3, file_name=FILE_NAME)

    S = get_scale(1, 3)
    vertices_h = (S @ vertices_h.T).T
    print_current_transformation(S=S, vertices=vertices_h, step_number=2, frame_number=3, file_name=FILE_NAME)

    R = get_rotation_matrix(60)
    vertices_h = (R @ vertices_h.T).T
    print_current_transformation(R=R, S=S, vertices=vertices_h, step_number=3, frame_number=3, file_name=FILE_NAME)

    rect = scene["rect"]
    rect.set_geometry(vertices_h[:, :2].flatten())
    rect["color"] = "green"


if __name__ == '__main__':
    scene = get_rectanglescene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.add_frames(frame3)
    scene.show()