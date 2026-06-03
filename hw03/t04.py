import numpy as np
from src.math.Rotations import rotation_matrix_x, rotation_matrix_y, rotation_matrix_z


def general_rotation_matrix(alpha, beta, gamma):
    Rx = rotation_matrix_x(alpha)
    Ry = rotation_matrix_y(beta)
    Rz = rotation_matrix_z(gamma)
    return Rz @ Ry @ Rx


def gimbal_lock_proof():
    alpha, beta, gamma = np.radians(30), np.radians(90), np.radians(45)

    print("=" * 60)
    print("1. General form: R = Rz(gamma) * Ry(beta) * Rx(alpha)")
    print("=" * 60)

    Rx = rotation_matrix_x(alpha)
    Ry = rotation_matrix_y(beta)
    Rz = rotation_matrix_z(gamma)

    print("\nRx(alpha) =")
    print(np.round(Rx, 4))
    print("\nRy(beta) =")
    print(np.round(Ry, 4))
    print("\nRz(gamma) =")
    print(np.round(Rz, 4))

    R = Rz @ Ry @ Rx
    print("\nR = Rz * Ry * Rx =")
    print(np.round(R, 4))

    print("\n" + "=" * 60)
    print("2. Substituting beta = pi/2: cos(beta)=0, sin(beta)=1")
    print("=" * 60)

    Ry_90 = rotation_matrix_y(np.pi / 2)
    R_lock = Rz @ Ry_90 @ Rx
    print("\nR at beta=90 =")
    print(np.round(R_lock, 4))

    print("\n" + "=" * 60)
    print("3. Simplification using trigonometric identities")
    print("=" * 60)
    print("""
At beta = pi/2, Ry = [[0, 0, 1], [0, 1, 0], [-1, 0, 0]].

R = Rz(gamma) * Ry(pi/2) * Rx(alpha) =

  [[  0,            sin(alpha-gamma),   cos(alpha-gamma)  ],
   [  0,            cos(alpha-gamma),  -sin(alpha-gamma)  ],
   [ -1,            0,                  0                 ]]

All elements depend only on the difference (alpha - gamma).
""")

    print("=" * 60)
    print("4. Proof of loss of one degree of freedom")
    print("=" * 60)

    deltas = [10, 20, -15]
    print("\nVerification: if alpha -> alpha+d, gamma -> gamma+d, R stays the same:")
    for delta in deltas:
        d = np.radians(delta)
        R_shifted = general_rotation_matrix(alpha + d, np.pi / 2, gamma + d)
        print(f"  d = {delta:+d}: R unchanged = {np.allclose(R_lock, R_shifted)}")

    print("\nConclusion: at beta=90, changing alpha and gamma by the same amount")
    print("does not affect the result => one degree of freedom is lost (Gimbal Lock).")


if __name__ == '__main__':
    gimbal_lock_proof()
