import numpy as np
from src.math.Quaternion import Quaternion
from src.math.Vec3 import Vec3


if __name__ == '__main__':
    u = Vec3(1, 1, 1).normalized()
    theta = np.radians(60)

    print("=" * 60)
    print("1. Quaternion construction")
    print("=" * 60)
    q = Quaternion.rotation(theta, u)
    print(f"  u = ({u.x:.4f}, {u.y:.4f}, {u.z:.4f})")
    print(f"  theta = 60 deg")
    print(f"  q = {q}")
    print(f"  q = (w={q.w:.6f}, x={q.x:.6f}, y={q.y:.6f}, z={q.z:.6f})")

    print("\n" + "=" * 60)
    print("2. Norm check")
    print("=" * 60)
    norm = q.norm()
    print(f"  |q| = {norm:.10f}")
    print(f"  |q| == 1: {np.isclose(norm, 1.0)}")

    print("\n" + "=" * 60)
    print("3. Rotation matrix R")
    print("=" * 60)
    R = q.toRotationMatrix()
    print("  R =")
    for i in range(4):
        row = [f"{R[i, j]:+.4f}" for j in range(4)]
        print(f"    [{', '.join(row)}]")

    R3 = np.array([[R[i, j] for j in range(3)] for i in range(3)])
    print(f"\n  R^T * R = I: {np.allclose(R3.T @ R3, np.eye(3), atol=1e-6)}")
    print(f"  det(R) = 1:  {np.isclose(np.linalg.det(R3), 1.0, atol=1e-6)}")
