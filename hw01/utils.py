import numpy as np
from RectangleScene import RectangleScene


def get_vertices():
    return np.array([[0, 0], [0, 1], [1, 1], [1, 0]], dtype=np.float64)


def get_homogeneous_vertices():
    return np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]], dtype=np.float64)


def get_rectanglescene():
    return RectangleScene(
        image_size=(10, 10),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-6, -6, 6, 6),  # розмірність системи координат
        title="Picture",  # заголовок рисунка
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-."  # стиль ліній осей координат
    )

def get_rotation_matrix(theta):

    theta = np.radians(theta)
    return np.array(
        [
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta),  0],
            [0,             0,              1]
        ],dtype=np.float64)


def get_translation(t_x, t_y):
    return np.array([
        [1,   0,   t_x],
        [0,   1,   t_y],
        [0,   0,     1]
    ], dtype=np.float64)


def get_scale(s_x, s_y):
    return np.array([
        [s_x, 0,   0],
        [0,   s_y, 0],
        [0,   0,   1]
    ], dtype=np.float64)


def get_rotation_around_pivot(theta, p_x, p_y):
    return get_translation(p_x, p_y) @ get_rotation_matrix(theta) @ get_translation(-p_x, -p_y)


def get_scale_around_pivot(sx, sy, p_x, p_y):
    return get_translation(p_x, p_y) @ get_scale(sx, sy) @ get_translation(-p_x, -p_y)


def print_current_transformation(R=None, T=None, S=None, vertices=None,
                                  step_number=0, frame_number=0,
                                  file_name="assets/t01.md"):
    R = R if R is not None else np.eye(3)
    T = T if T is not None else np.eye(3)
    S = S if S is not None else np.eye(3)
    M = T @ R @ S

    def mat_to_latex(mat):
        rows = " \\\\\n".join(
            " & ".join(f"{v:.3f}" for v in row)
            for row in mat
        )
        return f"$$\n\\begin{{pmatrix}}\n{rows}\n\\end{{pmatrix}}\n$$"

    labels = {"R": R, "T": T, "S": S, "$M=(T \\cdot R \\cdot S)$": M}

    with open(file_name, "a") as f:
        f.write(f"\n## Frame {frame_number}, Step {step_number}\n\n")
        for name, mat in labels.items():
            f.write(f"**{name}:**\n")
            f.write(mat_to_latex(mat))
            f.write("\n\n")

        if vertices is not None:
            f.write("**Vertices:**\n")
            f.write(mat_to_latex(vertices))
            f.write("\n\n")



if __name__ == '__main__':
    v = get_homogeneous_vertices()
    print(v)
    print_current_transformation()