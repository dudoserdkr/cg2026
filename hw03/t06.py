import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from hw02.utils import get_euler_rotation

ANGLES_A = np.array([0.0, 0.0, 0.0])
ANGLES_B = np.array([90.0, 90.0, 90.0])
N_STEPS = 10
FORWARD = np.array([0, 0, 1, 1], dtype=np.float64)


def lerp_euler_trajectory():
    trajectory = []
    for i in range(N_STEPS + 1):
        t = i / N_STEPS
        angles = (1 - t) * ANGLES_A + t * ANGLES_B
        R = get_euler_rotation("XYZ", angles.tolist())
        direction = (R @ FORWARD)[:3]
        trajectory.append(direction)
        print(f"Step {i:2d}: angles=({angles[0]:6.1f}, {angles[1]:6.1f}, {angles[2]:6.1f})"
              f"  -> forward=({direction[0]:+.4f}, {direction[1]:+.4f}, {direction[2]:+.4f})")
    return np.array(trajectory)


if __name__ == '__main__':
    traj = lerp_euler_trajectory()

    print("\nAs the middle angle (Y) approaches 90, Gimbal Lock occurs:")
    print("axes X and Z 'merge', interpolation becomes unnatural,")
    print("rotation speed is non-uniform, and the forward vector")
    print("trajectory makes abrupt direction changes.")

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], 'b-o', linewidth=2, markersize=5)
    ax.scatter(*traj[0], color='green', s=100, label='Start (0,0,0)')
    ax.scatter(*traj[-1], color='red', s=100, label='End (90,90,90)')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Euler Lerp trajectory of forward vector (0,0,1)')
    ax.legend()
    plt.tight_layout()
    plt.show()
