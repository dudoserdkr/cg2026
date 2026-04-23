import numpy as np
from Frame import Frame
from hw02.utils import get_cube_scene, get_cube_vertices, decompose_TRS
from constants import *

FILE_NAME = "assets/t12.md"

M = np.array([
    [0.707, -0.707,  0,     5],
    [1.060,  1.060, -1.0,  -2],
    [0.707,  0.707,  1.414, 3],
    [0,      0,      0,     1],
], dtype=np.float64)


def frame1(scene):
    (Frame(scene, "cube", get_cube_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "cube", get_cube_vertices, 2, FILE_NAME).
     apply(M).
     finish(FRAME_2))


if __name__ == '__main__':
    t, s, angle_deg, axis, R = decompose_TRS(M)

    print(f"Translation:    t = ({t[0]:.3f}, {t[1]:.3f}, {t[2]:.3f})")
    print(f"Scale:          s = ({s[0]:.3f}, {s[1]:.3f}, {s[2]:.3f})")
    print(f"Rotation angle: θ = {angle_deg:.3f}°")
    print(f"Rotation axis:  u = ({axis[0]:.3f}, {axis[1]:.3f}, {axis[2]:.3f})")
    print(f"R @ R.T ≈ I:    {np.allclose(R @ R.T, np.eye(3), atol=1e-2)}")
    print(f"det(R) ≈ 1:     {np.isclose(np.linalg.det(R), 1, atol=1e-2)}")

    scene = get_cube_scene()
    scene.add_frames(frame1, frame2)
    scene.show()