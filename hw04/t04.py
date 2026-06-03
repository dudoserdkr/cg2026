import numpy as np
from src.math.Quaternion import Quaternion
from src.math.Mat4x4 import Mat4x4
from src.math.utils_quat import rotation_matrix_to_quaternion


if __name__ == '__main__':
    R_3x3 = np.array([
        [0, -1, 0],
        [1,  0, 0],
        [0,  0, 1],
    ], dtype=np.float64)

    print("=" * 60)
    print("Rotation matrix R:")
    print("=" * 60)
    print(R_3x3)
    print(f"\nR^T * R = I: {np.allclose(R_3x3.T @ R_3x3, np.eye(3))}")
    print(f"det(R) = {np.linalg.det(R_3x3):.4f}")

    R_4x4 = Mat4x4(
        R_3x3[0, 0], R_3x3[0, 1], R_3x3[0, 2], 0,
        R_3x3[1, 0], R_3x3[1, 1], R_3x3[1, 2], 0,
        R_3x3[2, 0], R_3x3[2, 1], R_3x3[2, 2], 0,
        0,           0,           0,            1,
    )

    print("\n" + "=" * 60)
    print("Quaternion components q:")
    print("=" * 60)
    q = rotation_matrix_to_quaternion(R_4x4)
    print(f"  q = {q}")
    print(f"  w = {q.w:.6f}")
    print(f"  x = {q.x:.6f}")
    print(f"  y = {q.y:.6f}")
    print(f"  z = {q.z:.6f}")
    print(f"  |q| = {q.norm():.10f}")

    angle, axis = q.to_angle_axis()
    print(f"\n  Angle: {np.degrees(angle):.2f} deg")
    print(f"  Axis: ({axis.x:.4f}, {axis.y:.4f}, {axis.z:.4f})")

    R_reconstructed = q.toRotationMatrix()
    R_rec_3x3 = np.array([[R_reconstructed[i, j] for j in range(3)] for i in range(3)])
    print(f"\n  Reconstruction of R from q matches: {np.allclose(R_3x3, R_rec_3x3, atol=1e-6)}")
