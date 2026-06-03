import numpy as np
from src.math.Quaternion import Quaternion
from src.math.Vec3 import Vec3
from src.math.Vec4 import Vec4

VERTICES = [
    Vec3(0, 0, 0),
    Vec3(1, 0, 0),
    Vec3(0, 1, 0),
    Vec3(0, 0, 1),
]


if __name__ == '__main__':
    theta1 = np.radians(45)
    theta2 = np.radians(30)
    q1 = Quaternion.rotation_x(theta1)
    q2 = Quaternion.rotation_y(theta2)

    print("=" * 60)
    print("1. Individual rotation quaternions")
    print("=" * 60)
    print(f"  q1 (X 45 deg) = {q1}")
    print(f"  q2 (Y 30 deg) = {q2}")

    print("\n" + "=" * 60)
    print("2. Resultant quaternion q_total = q2 * q1")
    print("=" * 60)
    q_total = q2 * q1
    print(f"  q_total = {q_total}")
    print(f"  |q_total| = {q_total.norm():.10f}")

    print("\n" + "=" * 60)
    print("3. Total rotation parameters")
    print("=" * 60)
    angle, axis = q_total.to_angle_axis()
    print(f"  Angle: {np.degrees(angle):.4f} deg")
    print(f"  Axis: ({axis.x:.4f}, {axis.y:.4f}, {axis.z:.4f})")

    print("\n" + "=" * 60)
    print("4. New vertex coordinates (via quaternion algebra)")
    print("=" * 60)
    for i, v in enumerate(VERTICES):
        v_quat = Quaternion(0, v.x, v.y, v.z)
        v_rot = q_total * v_quat * q_total.conjugate()
        print(f"  V{i}: ({v.x:.0f},{v.y:.0f},{v.z:.0f}) -> "
              f"({v_rot.x:+.4f}, {v_rot.y:+.4f}, {v_rot.z:+.4f})")
