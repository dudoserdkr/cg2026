import numpy as np

from src.engine.model.Point import SimplePoint
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


FILE_NAME = "assets/t08.md"


def frame1(scene):
    rect_vertices = get_vertices()
    rect = scene["rect"]
    rect["color"] = "blue"
    rect.set_geometry(rect_vertices.flatten())
    print_current_transformation(vertices=rect_vertices, frame_number=1, step_number=1, file_name=FILE_NAME)


def frame2(scene):
    vertices_h = get_homogeneous_vertices() # vertices_h stands for homogeneous vertices

    S = get_scale_around_pivot(2, 3, 0.5, 0.5)
    vertices_h = (S @ vertices_h.T).T
    print_current_transformation(S=S, vertices=vertices_h, step_number=1, frame_number=2, file_name=FILE_NAME)

    rect = scene["rect"]
    rect.set_geometry(vertices_h[:, :2].flatten())
    rect["color"] = "red"

    pivot = SimplePoint(0.5, 0.5, color="red")
    # pivot["labels"] = (("$pivot\_2$", (0.5, 0.5)),)
    scene["pivot_2"] = pivot


def frame3(scene):
    vertices_h = get_homogeneous_vertices()  # vertices_h stands for homogeneous vertices

    S = get_scale_around_pivot(2, 3, 0, 1)
    vertices_h = (S @ vertices_h.T).T
    print_current_transformation(S=S, vertices=vertices_h, step_number=1, frame_number=3, file_name=FILE_NAME)

    rect = scene["rect"]
    rect.set_geometry(vertices_h[:, :2].flatten())
    rect["color"] = "green"

    pivot = SimplePoint(0, 1, color="green")
    # pivot["labels"] = (("$pivot\_3$", (0.1, 0.2)),)
    scene["pivot_3"] = pivot


def frame4(scene):
    vertices_h = get_homogeneous_vertices()  # vertices_h stands for homogeneous vertices

    S = get_scale_around_pivot(2, 3, 1, 1)
    vertices_h = (S @ vertices_h.T).T
    print_current_transformation(S=S, vertices=vertices_h, step_number=1, frame_number=4, file_name=FILE_NAME)

    rect = scene["rect"]
    rect.set_geometry(vertices_h[:, :2].flatten())
    rect["color"] = "orange"

    pivot = SimplePoint(1, 1, color="orange")
    # pivot["labels"] = (("$pivot\_4$", (1, 1)),)
    scene["pivot_4"] = pivot


def frame5(scene):
    vertices_h = get_homogeneous_vertices()  # vertices_h stands for homogeneous vertices

    S = get_scale_around_pivot(2, 3, 2, 2)
    vertices_h = (S @ vertices_h.T).T
    print_current_transformation(S=S, vertices=vertices_h, step_number=1, frame_number=5, file_name=FILE_NAME)

    rect = scene["rect"]
    rect.set_geometry(vertices_h[:, :2].flatten())
    rect["color"] = "black"

    pivot = SimplePoint(2, 2, color="black")
    scene["pivot_5"] = pivot


if __name__ == '__main__':
    scene = get_rectanglescene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.add_frames(frame3)
    scene.add_frames(frame4)
    scene.add_frames(frame5)
    scene.show()