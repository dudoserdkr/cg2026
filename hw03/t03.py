import numpy as np
from hw02.Frame import Frame
from hw02.utils import get_cube_scene, get_cube_vertices, get_euler_rotation
from hw02.constants import *

FILE_NAME = "assets/t03.md"

ANGLES = [45, 30, 60]


def frame1(scene):
    (Frame(scene, "cube", get_cube_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "cube", get_cube_vertices, 2, FILE_NAME).
     euler_rotate("XYZ", ANGLES).
     finish(FRAME_2))


def frame3(scene):
    (Frame(scene, "cube", get_cube_vertices, 3, FILE_NAME).
     euler_rotate("ZYX", ANGLES).
     finish(FRAME_3))


if __name__ == '__main__':
    R_xyz = get_euler_rotation("XYZ", ANGLES)
    R_zyx = get_euler_rotation("ZYX", ANGLES)

    print("R (XYZ extrinsic):")
    print(np.round(R_xyz, 4))
    print("\nR (ZYX extrinsic):")
    print(np.round(R_zyx, 4))
    print(f"\nMatrices equal: {np.allclose(R_xyz, R_zyx)}")

    v = get_cube_vertices()
    v_xyz = (R_xyz @ v.T).T
    v_zyx = (R_zyx @ v.T).T
    print("\nVertices after XYZ:")
    print(np.round(v_xyz[:, :3], 4))
    print("\nVertices after ZYX:")
    print(np.round(v_zyx[:, :3], 4))

    print("\nDifferent conventions apply rotations in a different order"
          " around the fixed (extrinsic) axes, so the same input angles"
          " produce different final orientations.")

    scene = get_cube_scene()
    scene.add_frames(frame1, frame2, frame3)
    scene.show()
