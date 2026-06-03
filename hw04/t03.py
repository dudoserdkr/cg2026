import numpy as np
from src.math.Quaternion import Quaternion
from hw02.utils import get_euler_rotation


if __name__ == '__main__':
    alpha, beta, gamma = 20.0, 90.0, 50.0
    alpha_r, beta_r, gamma_r = np.radians(alpha), np.radians(beta), np.radians(gamma)

    print("=" * 60)
    print("1. Quaternions for each rotation")
    print("=" * 60)
    qx = Quaternion.rotation_x(alpha_r)
    qy = Quaternion.rotation_y(beta_r)
    qz = Quaternion.rotation_z(gamma_r)
    print(f"  q_x (alpha={alpha} deg) = {qx}")
    print(f"  q_y (beta={beta} deg) = {qy}")
    print(f"  q_z (gamma={gamma} deg) = {qz}")

    print("\n" + "=" * 60)
    print("2. Final quaternion q = q_z * q_y * q_x")
    print("=" * 60)
    q = qz * qy * qx
    print(f"  q = {q}")
    print(f"  |q| = {q.norm():.10f}")

    angle, axis = q.to_angle_axis()
    print(f"  Rotation angle: {np.degrees(angle):.4f} deg")
    print(f"  Rotation axis: ({axis.x:.4f}, {axis.y:.4f}, {axis.z:.4f})")

    print("\n" + "=" * 60)
    print("3. Comparison with matrix approach")
    print("=" * 60)
    R_matrix = get_euler_rotation("XYZ", [alpha, beta, gamma])
    R_from_quat = q.normalized().toRotationMatrix()

    print("  Matrix (via Euler):")
    print(np.round(np.array([[R_matrix[i, j] for j in range(4)] for i in range(4)]), 4))
    print("\n  Matrix (from quaternion):")
    R_q = np.array([[R_from_quat[i, j] for j in range(4)] for i in range(4)])
    print(np.round(R_q, 4))

    print(f"\n  Matrices match: {np.allclose(R_matrix[:3, :3], R_q[:3, :3], atol=1e-4)}")

    print("\n" + "=" * 60)
    print("4. Why quaternions do not have the Gimbal Lock problem")
    print("=" * 60)
    print("  Quaternion q uniquely defines orientation without loss of")
    print("  degrees of freedom. Unlike Euler angles, where at beta=90")
    print("  axes X and Z 'merge' and we cannot distinguish separate")
    print("  rotations around them, the quaternion preserves full information:")
    print(f"  q = {q}")
    print(f"  Angle = {np.degrees(angle):.4f} deg, axis = ({axis.x:.4f}, {axis.y:.4f}, {axis.z:.4f})")

    q_perturbed = qz * qy * Quaternion.rotation_x(np.radians(alpha + 5))
    print(f"\n  q(alpha+5 deg) = {q_perturbed}")
    print(f"  q != q(alpha+5 deg): {not np.allclose(q.q, q_perturbed.q, atol=1e-6)}")
    print("  -> Quaternion is sensitive to alpha change even at beta=90.")
