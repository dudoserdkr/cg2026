import numpy as np
from hw02.Frame import Frame
from hw02.utils import get_cube_scene, get_cube_vertices, get_rotation
from hw02.constants import *

FILE_NAME = "assets/t05.md"


def _intrinsic_xyz(alpha, beta, gamma):
    Rx = get_rotation([1, 0, 0], alpha)
    Ry = get_rotation([0, 1, 0], beta)
    Rz = get_rotation([0, 0, 1], gamma)
    return Rx @ Ry @ Rz


def frame1(scene):
    (Frame(scene, "cube", get_cube_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "cube", get_cube_vertices, 2, FILE_NAME, local=True).
     rotate([1, 0, 0], 30).
     rotate([0, 1, 0], 90).
     rotate([0, 0, 1], 45).
     finish(FRAME_2))


def frame3(scene):
    (Frame(scene, "cube", get_cube_vertices, 3, FILE_NAME, local=True).
     rotate([1, 0, 0], 40).
     rotate([0, 1, 0], 90).
     rotate([0, 0, 1], 35).
     finish(FRAME_3))


if __name__ == '__main__':
    R_original = _intrinsic_xyz(30, 90, 45)
    R_modified = _intrinsic_xyz(40, 90, 35)

    v = get_cube_vertices()
    v_orig = (R_original @ v.T).T
    v_mod = (R_modified @ v.T).T

    print("Cube vertices after intrinsic XYZ (30, 90, 45):")
    print(np.round(v_orig[:, :3], 4))
    print("\nCube vertices after intrinsic XYZ (40, 90, 35):")
    print(np.round(v_mod[:, :3], 4))

    print(f"\nMatrices equal: {np.allclose(R_original, R_modified)}")
    print(f"Coordinates equal: {np.allclose(v_orig, v_mod)}")

    print("\nFor intrinsic XYZ (R = Rx*Ry*Rz) at beta=90,")
    print("the matrix depends only on the sum (alpha + gamma).")
    print(f"Original: alpha+gamma = 30+45 = 75")
    print(f"Modified: alpha+gamma = 40+35 = 75")
    print("Sums are equal => cube position is unchanged => axes X and Z are 'glued'.")

    scene = get_cube_scene()
    scene.add_frames(frame1, frame2, frame3)
    scene.show()
