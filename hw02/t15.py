import numpy as np
from Frame import Frame
from hw02.utils import (
    get_cube_scene, get_cube_vertices, decompose_TRS,
    get_scale_around_pivot, get_rotation, get_translation,
)
from constants import *

FILE_NAME = "assets/t15.md"


def frame1(scene):
    (Frame(scene, "cube", get_cube_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "cube", get_cube_vertices, 2, FILE_NAME).
     scale_around_pivot([2, 2, 2], [1, 1, 1]).
     finish(FRAME_2))


def frame3(scene):
    (Frame(scene, "cube", get_cube_vertices, 3, FILE_NAME).
     scale_around_pivot([2, 2, 2], [1, 1, 1]).
     rotate([0, 1, 0], 90, local=True).
     finish(FRAME_3))


def frame4(scene):
    (Frame(scene, "cube", get_cube_vertices, 4, FILE_NAME).
     scale_around_pivot([2, 2, 2], [1, 1, 1]).
     rotate([0, 1, 0], 90, local=True).
     translate([-3, 4, 2]).
     finish(FRAME_4))


if __name__ == '__main__':
    # Build final matrix manually for decomposition
    M_scale = get_scale_around_pivot([2, 2, 2], [1, 1, 1])
    R_y    = get_rotation([0, 1, 0], 90)
    T      = get_translation([-3, 4, 2])

    M = M_scale
    M = M @ R_y
    M = T @ M

    t, s, angle_deg, axis, R = decompose_TRS(M)
    print(f"Translation:    t = ({t[0]:.3f}, {t[1]:.3f}, {t[2]:.3f})")
    print(f"Scale:          s = ({s[0]:.3f}, {s[1]:.3f}, {s[2]:.3f})")
    print(f"Rotation angle: θ = {angle_deg:.3f}°")
    print(f"Rotation axis:  u = ({axis[0]:.3f}, {axis[1]:.3f}, {axis[2]:.3f})")

    scene = get_cube_scene()
    scene.add_frames(frame1, frame2, frame3, frame4)
    scene.show()

    # Translation: t = (-4.000, 3.000, 1.000)
    # Scale: s = (2.000, 2.000, 2.000)
    # Rotation
    # angle: θ = 90.000°
    # Rotation
    # axis: u = (0.000, 1.000, 0.000)
