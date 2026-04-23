import numpy as np
from hw02.scenes.CubeScene import CubeScene
from hw02.scenes.TetrahedronScene import TetrahedronScene
from hw02.scenes.TriangleScene import TriangleScene
from hw02.scenes.RectangleScene import RectangleScene

_SCENE_DEFAULTS = dict(
    image_size=(10, 10),
    coordinate_rect=(-8, -8, -8, 10, 10, 10),
    title="Picture",
    grid_show=False,
    base_axis_show=False,
    axis_show=True,
    axis_color=("red", "green", "blue"),
    axis_line_style="-.",
)


def get_cube_scene(**kwargs):
    return CubeScene(**{**_SCENE_DEFAULTS, **kwargs})


def get_tetrahedron_scene(vertices=None, **kwargs):
    return TetrahedronScene(vertices=vertices, **{**_SCENE_DEFAULTS, **kwargs})


def get_triangle_scene(vertices=None, **kwargs):
    return TriangleScene(vertices=vertices, **{**_SCENE_DEFAULTS, **kwargs})


def get_rectangle_scene(vertices=None, **kwargs):
    return RectangleScene(vertices=vertices, **{**_SCENE_DEFAULTS, **kwargs})


def get_cube_vertices():
    return np.array([
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 1, 1],
        [0, 1, 1, 1],
    ], dtype=np.float64)


def get_tetrahedron_vertices():
    """Task 5, 13. Standard tetrahedron at origin."""
    return np.array([
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
    ], dtype=np.float64)


def get_triangle_vertices():
    """Task 8. Triangle with vertices (1,2,3), (4,5,6), (7,8,9)."""
    return np.array([
        [1, 2, 3, 1],
        [4, 5, 6, 1],
        [7, 8, 9, 1],
    ], dtype=np.float64)


def get_rectangle_vertices():
    """Task 9. Rectangle in XY plane."""
    return np.array([
        [1, 2, 0, 1],
        [4, 2, 0, 1],
        [4, 5, 0, 1],
        [1, 5, 0, 1],
    ], dtype=np.float64)


def set_obj_color(obj, color, edge_color):
    for p in obj.polygons:
        p.color = color
        p.edgecolor = edge_color


def get_skew_matrix(t):
    x, y, z = t
    return np.array([
        [0, -z, y],
        [z, 0, -x],
        [-y, x, 0]
    ], dtype=np.float64)


def _rodrigues_formula(axis, angle):
    axis = np.asarray(axis)
    axis = axis / np.linalg.norm(axis)
    skew_matrix = get_skew_matrix(axis)
    theta = np.radians(angle)
    R = np.eye(3) + np.sin(theta) * skew_matrix + (1 - np.cos(theta)) * (skew_matrix @ skew_matrix)
    return R


def get_rotation(axis, angle):
    R = np.eye(4)
    R[:3, :3] = _rodrigues_formula(axis, angle)
    return R


def get_euler_rotation(convention: str, angles):
    convention_dict = {"X": [1, 0, 0], "Y": [0, 1, 0], "Z": [0, 0, 1]}
    R = np.eye(4, dtype=np.float64)
    for i in range(3):
        axis = convention_dict[convention[i]]
        angle = angles[i]
        R = get_rotation(axis, angle) @ R
    return R


def get_scale(s):
    S = np.eye(4, dtype=np.float64)
    for i in range(3):
        S[i, i] = s[i]
    return S


def get_translation(t):
    T = np.eye(4, dtype=np.float64)
    T[:3, 3] = t
    return T


def get_rotation_around_pivot(axis, angle, pivot):
    pivot = np.asarray(pivot)
    return get_translation(pivot) @ get_rotation(axis, angle) @ get_translation(-pivot)

def get_scale_around_pivot(s, pivot):
    pivot = np.asarray(pivot)
    return get_translation(pivot) @ get_scale(s) @ get_translation(-pivot)


def print_current_transformation(M_step=None, M_total=None, vertices=None,
                                  step_number=0, frame_number=0,
                                  file_name="assets/t01.md"):
    def mat_to_latex(mat):
        rows = " \\\\\n".join(
            " & ".join(f"{v:.3f}" for v in row)
            for row in mat
        )
        return f"$$\n\\begin{{pmatrix}}\n{rows}\n\\end{{pmatrix}}\n$$"

    with open(file_name, "a") as f:
        f.write(f"\n## Frame {frame_number}, Step {step_number}\n\n")
        if M_step  is not None: f.write(f"**$M_{{step}}$:**\n{mat_to_latex(M_step)}\n\n")
        if M_total is not None: f.write(f"**$M_{{total}}$:**\n{mat_to_latex(M_total)}\n\n")
        if vertices is not None:
            f.write(f"**Vertices:**\n{mat_to_latex(vertices)}\n\n")


import numpy as np


def decompose_TRS(M):
    t = M[:3, 3]

    A = M[:3, :3]
    s = np.linalg.norm(A, axis=0)

    R = A / s

    cos_theta = np.clip((np.trace(R) - 1) / 2, -1.0, 1.0)
    theta = np.arccos(cos_theta)

    if np.isclose(np.sin(theta), 0):
        axis = np.array([1.0, 0.0, 0.0])
    else:
        axis = np.array([
            R[2, 1] - R[1, 2],
            R[0, 2] - R[2, 0],
            R[1, 0] - R[0, 1],
        ]) / (2 * np.sin(theta))

    return t, s, np.degrees(theta), axis, R


if __name__ == '__main__':
    print(get_rotation([1, 1, 0], 45))
    print(get_translation((2, 2, 2)))