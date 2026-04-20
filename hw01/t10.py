import numpy as np
from utils import (
    get_vertices,
    get_rectanglescene,
    get_homogeneous_vertices,
    get_scale,
    get_translation,
    get_rotation_matrix,
    print_current_transformation,
    get_scale_around_pivot
)


FILE_NAME = "assets/t10.md"


def frame1(scene):
    rect_vertices = get_vertices()
    rect = scene["rect"]
    rect["color"] = "blue"
    rect.set_geometry(rect_vertices.flatten())
    print_current_transformation(vertices=rect_vertices, frame_number=1, step_number=1, file_name=FILE_NAME)


def frame2(scene):
    vertices_h = get_homogeneous_vertices() # vertices_h stands for homogeneous vertices

    R = T = S = np.eye(3)

    S = get_scale(2, 2)
    vertices_h = (S @ vertices_h.T).T
    print_current_transformation(R=R, T=T, S=S, vertices=vertices_h, step_number=1, frame_number=2, file_name=FILE_NAME)

    R = get_rotation_matrix(30)
    vertices_h = (R @ vertices_h.T).T
    print_current_transformation(R=R, T=T, S=S, vertices=vertices_h, step_number=2, frame_number=2, file_name=FILE_NAME)

    T = get_translation(1, -1)
    vertices_h = (T @ vertices_h.T).T
    print_current_transformation(R=R, T=T, S=S, vertices=vertices_h, step_number=3, frame_number=2, file_name=FILE_NAME)


    rect = scene["rect"]
    rect.set_geometry(vertices_h[:, :2].flatten())
    rect["color"] = "red"


def frame3(scene):
    vertices_h = get_homogeneous_vertices()  # vertices_h stands for homogeneous vertices

    R = T = S = np.eye(3)

    T = get_translation(1, -1)
    vertices_h = (T @ vertices_h.T).T
    print_current_transformation(R=R, T=T, S=S, vertices=vertices_h, step_number=1, frame_number=3, file_name=FILE_NAME)

    S = get_scale(2, 2)
    vertices_h = (S @ vertices_h.T).T
    print_current_transformation(R=R, T=T, S=S, vertices=vertices_h, step_number=2, frame_number=3, file_name=FILE_NAME)

    R = get_rotation_matrix(30)
    vertices_h = (R @ vertices_h.T).T
    print_current_transformation(R=R, T=T, S=S, vertices=vertices_h, step_number=3, frame_number=3, file_name=FILE_NAME)

    rect = scene["rect"]
    rect.set_geometry(vertices_h[:, :2].flatten())
    rect["color"] = "green"


def frame4(scene):
    vertices_h = get_homogeneous_vertices()  # vertices_h stands for homogeneous vertices

    R = T = S = np.eye(3)

    S = get_scale(2, 2)
    vertices_h = (S @ vertices_h.T).T
    print_current_transformation(R=R, T=T, S=S, vertices=vertices_h, step_number=1, frame_number=4, file_name=FILE_NAME)

    T = get_translation(1, -1)
    vertices_h = (T @ vertices_h.T).T
    print_current_transformation(R=R, T=T, S=S, vertices=vertices_h, step_number=2, frame_number=4, file_name=FILE_NAME)

    R = get_rotation_matrix(30)
    vertices_h = (R @ vertices_h.T).T
    print_current_transformation(R=R, T=T, S=S, vertices=vertices_h, step_number=3, frame_number=4, file_name=FILE_NAME)

    rect = scene["rect"]
    rect.set_geometry(vertices_h[:, :2].flatten())
    rect["color"] = "black"


if __name__ == '__main__':
    scene = get_rectanglescene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.add_frames(frame3)
    scene.add_frames(frame4)
    scene.show()