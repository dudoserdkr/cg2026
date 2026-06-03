import numpy as np
from hw02.utils import get_euler_rotation


def euler_from_matrix_xyz_extrinsic(R):
    if R.shape[0] == 4:
        R = R[:3, :3]

    neg_sin_beta = np.clip(R[2, 0], -1.0, 1.0)

    if np.isclose(abs(neg_sin_beta), 1.0, atol=1e-6):
        beta = np.arcsin(-neg_sin_beta)
        alpha = 0.0
        if neg_sin_beta < 0:
            gamma = -np.arctan2(R[0, 1], R[0, 2])
        else:
            gamma = np.arctan2(-R[0, 1], R[0, 2])
        print(f"  [!] Gimbal Lock: beta={np.degrees(beta):.1f} deg, fixing alpha=0")
    else:
        beta = np.arcsin(-neg_sin_beta)
        cos_beta = np.cos(beta)
        alpha = np.arctan2(R[2, 1] / cos_beta, R[2, 2] / cos_beta)
        gamma = np.arctan2(R[1, 0] / cos_beta, R[0, 0] / cos_beta)

    return alpha, beta, gamma


if __name__ == '__main__':
    print("=" * 60)
    print("1. Rotation matrix R with beta=90 around Y (Gimbal Lock)")
    print("=" * 60)

    R_full = get_euler_rotation("XYZ", [30, 90, 45])
    R = R_full[:3, :3]
    print(f"R[2,0] = {R[2, 0]:.4f} (= -sin(beta), expect -1)")
    print("R =")
    print(np.round(R, 4))

    print("\n" + "=" * 60)
    print("2. Infinite number of (alpha, gamma) combinations")
    print("=" * 60)
    print("\nAt beta=90 (extrinsic XYZ), R depends only on (alpha - gamma).")
    print("Any pair (alpha, gamma) with the same difference gives the same matrix:")

    alpha_0, gamma_0 = np.radians(30), np.radians(45)
    diff = alpha_0 - gamma_0
    print(f"\nOriginal: alpha={np.degrees(alpha_0):.0f}, gamma={np.degrees(gamma_0):.0f}, alpha-gamma={np.degrees(diff):.0f}")

    for offset in [0, 20, -30, 50, 90]:
        a = alpha_0 + np.radians(offset)
        g = gamma_0 + np.radians(offset)
        R_test = get_euler_rotation("XYZ", [np.degrees(a), 90, np.degrees(g)])[:3, :3]
        same = np.allclose(R, R_test, atol=1e-6)
        print(f"  alpha={np.degrees(a):+7.1f}, gamma={np.degrees(g):+7.1f} -> R unchanged: {same}")

    print("\n" + "=" * 60)
    print("3. Stable solution: alpha=0 at singularity")
    print("=" * 60)
    alpha, beta, gamma = euler_from_matrix_xyz_extrinsic(R)
    print(f"  alpha = {np.degrees(alpha):.2f}")
    print(f"  beta  = {np.degrees(beta):.2f}")
    print(f"  gamma = {np.degrees(gamma):.2f}")

    R_reconstructed = get_euler_rotation("XYZ",
        [np.degrees(alpha), np.degrees(beta), np.degrees(gamma)])[:3, :3]
    print(f"\n  Reconstruction matches original: {np.allclose(R, R_reconstructed, atol=1e-6)}")
