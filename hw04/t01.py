import numpy as np
from src.math.Quaternion import Quaternion
from src.math.Vec3 import Vec3


if __name__ == '__main__':
    p = Vec3(1, 0, 0)
    theta = np.radians(90)
    q = Quaternion.rotation_z(theta)

    print("=" * 60)
    print("1. Point p as pure quaternion v = (0, 1, 0, 0)")
    print("=" * 60)
    v = Quaternion(0, p.x, p.y, p.z)
    print(f"  p = ({p.x}, {p.y}, {p.z})")
    print(f"  v = {v}")
    print(f"  q (rot Z 90 deg) = {q}")

    print("\n" + "=" * 60)
    print("2. Rotation: v' = q * v * q^-1")
    print("=" * 60)
    v_rotated = q * v * q.inverse()
    print(f"  v' = {v_rotated}")
    p_new = Vec3(v_rotated.x, v_rotated.y, v_rotated.z)
    print(f"  New coordinates: ({p_new.x:.4f}, {p_new.y:.4f}, {p_new.z:.4f})")

    print("\n" + "=" * 60)
    print("3. Verification with matrix transformation")
    print("=" * 60)
    R = q.toRotationMatrix()
    p_matrix = q.rotate_vector(p)
    print(f"  Via rotate_vector: ({p_matrix.x:.4f}, {p_matrix.y:.4f}, {p_matrix.z:.4f})")

    expected = Vec3(0, 1, 0)
    print(f"  Expected result: ({expected.x}, {expected.y}, {expected.z})")
    print(f"  Matches expected: {np.allclose([p_new.x, p_new.y, p_new.z], [0, 1, 0], atol=1e-6)}")
