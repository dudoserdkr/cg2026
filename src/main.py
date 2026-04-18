import numpy as np

from src.engine.model.Polygon import Polygon
from src.engine.scene.Scene import Scene

if __name__ == '__main__':
    FIGURE_KEY = "polygon"


    class SampleScene(Scene):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            polygon = Polygon()
            self[FIGURE_KEY] = polygon

            # Задаємо геометрію - пара послідовних значень визначає вершину на площині
            polygon.set_geometry(
                0, 0,
                2, 0,
                2, 1,
                1, 2,
                0, 1
            )


    def frame1(scene):
        polygon = scene[FIGURE_KEY]
        # Задаємо параметри полігону
        polygon["color"] = "blue"  # колір ліній
        polygon["line_style"] = "--"  # стиль ліній
        polygon["vertices_show"] = True  # показувати вершини
        polygon["vertex_color"] = "grey"  # колір вершин
        polygon["labels"] = [  # підписи верших зі зміщеннями
            (r'$P_1$', (-0.2, -0.6)),
            (r'$P_2$', (0.2, -0.2)),
            (r'$P_3$', (-0.1, 0.2)),
            (r"$P_4$", (-0.2, 0.3)),
            (r"$P_5$", (-0.7, -0.2)),
        ]

        # задаємо трансформацію
        polygon.scale = (2, 1)  # масштабування
        polygon.rotation = (np.radians(45))  # поворот
        polygon.translation = (2, 1)  # перенесення



    scene = SampleScene(
        image_size=(5, 5),  # розмір зображення: 1 - 100 пікселів
        coordinate_rect=(-1, -1, 6, 6),  # розмірність системи координат
        title="Picture",  # заголовок рисунка
        grid_show=False,  # чи показувати координатну сітку
        base_axis_show=False,  # чи показувати базові осі зображення
        axis_show=True,  # чи показувати осі координат
        axis_color=("red", "green"),  # колір осей координат
        axis_line_style="-."  # стиль ліній осей координат
    )

    scene.add_frames(frame1)
    scene.show()
