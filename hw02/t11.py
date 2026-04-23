import numpy as np
from Frame import Frame
from hw02.utils import get_cube_scene, get_cube_vertices, get_rotation
from constants import *

FILE_NAME = "assets/t11.md"


def frame1(scene):
    (Frame(scene, "cube", get_cube_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "cube", get_cube_vertices, 2, FILE_NAME).
     rotate([1, 0, 0], 30).
     rotate([0, 1, 0], 45).
     rotate([0, 0, 1], 60).
     finish(FRAME_2))


def frame3(scene):
    (Frame(scene, "cube", get_cube_vertices, 3, FILE_NAME, local=True).
     rotate([0, 0, 1], 60).
     rotate([0, 1, 0], 45).
     rotate([1, 0, 0], 30).
     finish(FRAME_3))


if __name__ == '__main__':
    Rx = get_rotation([1, 0, 0], 30)
    Ry = get_rotation([0, 1, 0], 45)
    Rz = get_rotation([0, 0, 1], 60)

    R_A = Rz @ Ry @ Rx
    R_B = Rz @ Ry @ Rx

    print("R_A (extrinsic XYZ):")
    print(np.round(R_A, 4))
    print("\nR_B (intrinsic ZYX):")
    print(np.round(R_B, 4))
    print(f"\nR_A == R_B: {np.allclose(R_A, R_B)}")
    print(f"Max difference: {np.max(np.abs(R_A - R_B)):.2e}")

    scene = get_cube_scene()
    scene.add_frames(frame1, frame2, frame3)
    scene.show()

# R_A (extrinsic XYZ):
# [[ 0.3536 -0.5732  0.7392  0.    ]
#  [ 0.6124  0.7392  0.2803  0.    ]
#  [-0.7071  0.3536  0.6124  0.    ]
#  [ 0.      0.      0.      1.    ]]
#
# R_B (intrinsic ZYX):
# [[ 0.3536 -0.5732  0.7392  0.    ]
#  [ 0.6124  0.7392  0.2803  0.    ]
#  [-0.7071  0.3536  0.6124  0.    ]
#  [ 0.      0.      0.      1.    ]]
#
# R_A == R_B: True
# Max difference: 0.00e+00
