import numpy as np
from src.math.Quaternion import Quaternion
from src.math.Mat4x4 import Mat4x4
from src.math.utils_quat import rotation_matrix_to_quaternion
from hw02.Frame import Frame
from hw02.utils import get_cube_scene, get_cube_vertices, set_obj_color
from hw02.constants import *


M = np.array([
    [0,  -2,  0,   10],
    [1,   0,  0,   -5],
    [0,   0,  1.5,  3],
    [0,   0,  0,    1],
], dtype=np.float64)


if __name__ == '__main__':
    print("=" * 60)
    print("Input matrix M:")
    print("=" * 60)
    print(M)

    print("\n" + "=" * 60)
    print("1. Extracting translation T")
    print("=" * 60)
    T = M[:3, 3]
    print(f"  T = ({T[0]:.1f}, {T[1]:.1f}, {T[2]:.1f})")

    print("\n" + "=" * 60)
    print("2. Extracting scale S")
    print("=" * 60)
    A = M[:3, :3]
    sx = np.linalg.norm(A[:, 0])
    sy = np.linalg.norm(A[:, 1])
    sz = np.linalg.norm(A[:, 2])
    print(f"  S = ({sx:.4f}, {sy:.4f}, {sz:.4f})")

    print("\n" + "=" * 60)
    print("3. Pure rotation matrix R")
    print("=" * 60)
    R = np.zeros((3, 3))
    R[:, 0] = A[:, 0] / sx
    R[:, 1] = A[:, 1] / sy
    R[:, 2] = A[:, 2] / sz
    print("  R =")
    print(np.round(R, 4))
    print(f"\n  R^T * R = I: {np.allclose(R.T @ R, np.eye(3), atol=1e-6)}")
    print(f"  det(R) = {np.linalg.det(R):.4f}")

    print("\n" + "=" * 60)
    print("4. Converting R to quaternion q")
    print("=" * 60)
    R_4x4 = Mat4x4(
        R[0, 0], R[0, 1], R[0, 2], 0,
        R[1, 0], R[1, 1], R[1, 2], 0,
        R[2, 0], R[2, 1], R[2, 2], 0,
        0,       0,       0,       1,
    )
    q = rotation_matrix_to_quaternion(R_4x4)
    print(f"  q = {q}")
    print(f"  w = {q.w:.6f}")
    print(f"  x = {q.x:.6f}")
    print(f"  y = {q.y:.6f}")
    print(f"  z = {q.z:.6f}")
    print(f"  |q| = {q.norm():.10f}")

    angle, axis = q.to_angle_axis()
    print(f"\n  Rotation angle: {np.degrees(angle):.2f} deg")
    print(f"  Rotation axis: ({axis.x:.4f}, {axis.y:.4f}, {axis.z:.4f})")

    T_mat = np.eye(4)
    T_mat[:3, 3] = T
    R_mat = np.eye(4)
    R_mat[:3, :3] = R
    S_mat = np.diag([sx, sy, sz, 1.0])
    M_reconstructed = T_mat @ R_mat @ S_mat
    print(f"\n  M = T * R * S reconstruction matches: {np.allclose(M, M_reconstructed, atol=1e-6)}")
