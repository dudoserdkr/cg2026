import numpy as np

from RectangleScene import RectangleScene
from engine.model.BaseModel import BaseModel
from utils import get_vertices, rotation_matrix_2d


def frame1(scene):
    rect_vertices = get_vertices()
    rect = scene["rect"]
    rect["color"] = "blue"
    rect.set_geometry(rect_vertices.flatten())


def frame2(scene):
    vertices = get_vertices()
    theta = np.radians(30)
    R = rotation_matrix_2d(theta)
    print(R)
    print((R @ vertices.T).T)
    t = np.array([2, 3])
    print(t)
    transformed_vertices = (R @ vertices.T).T + t
    print(transformed_vertices)

    rect = scene["rect"]
    rect.set_geometry(transformed_vertices.flatten())
    rect["color"] = "red"




if __name__ == '__main__':

    scene = RectangleScene(
        image_size=(5, 5),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-1, -1, 6, 6),  # розмірність системи координат
        title="Picture",  # заголовок рисунка
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-."  # стиль ліній осей координат
    )
    # scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.show()