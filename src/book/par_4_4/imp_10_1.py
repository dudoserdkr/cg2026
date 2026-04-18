import numpy
import numpy as np

from engine.model.Axis import Axis
from engine.model.LineModel import LineModel
from src.base.lines import draw_line
from src.base.points import draw_points
from src.base.poligon import draw_poly
from src.math.Vec3 import Vec3
from src.engine.scene.Scene import Scene

if __name__ == '__main__':
    def frame1(self):
            # Координати вершин багатокутника
            # x = [1, 3, 4, 2]
            # y = [1, 1, 3, 4]

            vertices = [
                numpy.array((-1, -1)),
                numpy.array((1, -1)),
                numpy.array((1, 1)),
                numpy.array((-1, 1)),
            ]

            points = [
                (-1, 0),
                (1, 0),
                (1, 1),
                # (0, -1),
                (-1, 1),

            ]

            draw_points(points,
            vertices_show = True,
            labels = [('-1', (-0.25, 0.1)),
                      ('1', (0.05, 0.1)),
                      # ('1',(0.05, 0.1)),
                      # ('-1',(0.05, -0.25)),
                      ("$P'$",(0.05, 0.1)),
                      ("$S'$",(0.05, 0.1)),
                      ],  # Підписи вершин
            vertex_color = "red",
            )

            draw_poly(
                # x, y,
                vertices,
                alpha=0.5,
                solid_line=True,
                # edgecolor="#5B86AD",
                # vertices_show=True,
                # vertex_size=100,
                linewidth=1,
                fill_color="#C1D5A4",
            )

            draw_line(
                (-1, -1),(1, -1),
                color="#5B86AD",
                linewidth=5,
            )
            draw_line(
                (-1, 1),(1, 1),
                color="#5B86AD",
                linewidth=5,
            )


    O = np.array([0, 0])
    x = Vec3(1, 0)
    y = Vec3(0, 1)

    scene = Scene(
        title="",
        coordinate_rect=(-2, -2, 2, 2),
        grid_show=False,
        base_axis_show=False,
        axis_show=False,
        axis_color=("brown", "brown"),
        axis_line_style="-."
    )

    Oy = Axis(0, -1.4, 0, 1.4, color="brown", linewidth=1.5, line_style="--",
              label="$Y$", label_offset=(0.1, 0.2))
    Oz = Axis(-1.4, 0, 1.4, 0, color="brown", linewidth=1.5, line_style="--",
              label="$Z$", label_offset=(0.05, 0.1))
    scene["OZ_ID"] = Oz
    scene["OY_ID"] = Oy

    near = LineModel(-1, -1.2, -1, 1.2, color="green", linewidth=4., line_style="--", )
    far = LineModel(1, -1.2, 1, 1.2, color="blue", linewidth=4., line_style="--", )
    scene["near"] = near
    scene["far"] = far

    scene.add_frames(frame1)
    scene.show()
