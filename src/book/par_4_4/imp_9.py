import numpy as np

from base.arc import draw_arc
from base.poligon import draw_poly
from src.base.points import draw_points
from src.base.text import print_label
from src.engine.model.Axis import Axis
from src.engine.model.LineModel import LineModel
from src.engine.scene.Scene import Scene
from src.math.Vec3 import Vec3

f = 1.8
n = 0.7
alpha = np.radians(25)

if __name__ == '__main__':
    def frame1(self):
        vertices = [
            (n, -n* np.tan(alpha)),
            (n, n* np.tan(alpha)),
            (f, f * np.tan(alpha)),
            (f, -f * np.tan(alpha)),
        ]


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

        points = [
            (0, 0),
            (f, f * np.tan(alpha)),
            (f, 0),
            (n, n * np.tan(alpha)),
            (n, 0,),
        ]

        draw_points(points,
                    vertices_show=True,
                    labels=[
                        ("O", (-0.1, -0.2)),
                        # ("$P(y, z)$", (-0.3, 0.1)),
                        ("$P$", (0.05, -0.1)),
                        ('$F$', (0.05, -0.15)),
                        # ("$S(y',d)$", (-0.35, 0.1)),
                        ("$S$", (-0.15, 0.05)),
                        ("$N$", (-0.15, -0.15)),
                    ],  # Підписи вершин
                    vertex_color="red",
                    )

        print_label(start=(n, 0.8),
                    label="near\nplane",
                    # label_color="green",
                    # label_fontsize=13,
                    label_offset=(-0.15, 0.)
                    )

        print_label(start=(f, 1.),
                    label="far\nplane",
                    # label_color="green",
                    # label_fontsize=13,
                    label_offset=(-0.15, 0.05)
                    )

        draw_arc(O, (f, f * np.tan(alpha)), (f, -f * np.tan(alpha)),
                 radius=0.3,
                 color="brown",
                 # linestyle="--",
                 linewidth=3.0,
                 )

        print_label(start=O,
                    label=r"$\alpha$",
                    # label_fontsize=LABEL_FONT_SIZE,
                    label_offset=(0.35, 0.05)
                    )

    O = np.array([0, 0])
    x = Vec3(1, 0)
    y = Vec3(0, 1)

    scene = Scene(
        title="",
        coordinate_rect=(-0.5, -1.5, 2.5, 1.5),
        grid_show=False,
        base_axis_show=False,
        axis_show=False,
        axis_color=("brown", "brown"),
        axis_line_style="-."
    )

    f1 = f + 0.3
    line_top    = LineModel(0, 0, f1, f1 * np.tan(alpha), color="#5B86AD", linewidth=5)
    line_bottom = LineModel(0, 0, f1, -f1 * np.tan(alpha), color="#5B86AD", linewidth=5)

    Oz = Axis(0, 0, 2.2, 0, color="brown", linewidth=1.5, line_style="--",
              label="$-Z$", label_offset=(0.1, 0.1))
    Oy = Axis(0, -0, 0, 1.2, color="brown", linewidth=1.5, line_style="--",
              label="$Y$", label_offset=(0.1, 0.05))
    near = LineModel(n, -0.7, n, 0.7, color="green", linewidth=3., line_style="--", )
    far = LineModel(f, -0.99, f, 0.99, color="green", linewidth=3., line_style="--", )

    scene["OZ_ID"] = Oz
    scene["oy"] = Oy
    scene["near"] = near
    scene["far"] = far
    scene["line"] = line_top
    scene["line_bottom"] = line_bottom

    scene.add_frames(frame1)
    scene.show()
