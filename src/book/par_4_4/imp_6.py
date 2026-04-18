import numpy as np

from src.engine.model.Axis import Axis
from src.engine.model.LineModel import LineModel
from src.base.points import draw_points
from src.base.text import print_label
from src.engine.scene.Scene import Scene
from src.math.Vec3 import Vec3

if __name__ == '__main__':
    def frame1(self):

            points = [
                (0, 0),
                (1.5, 0.75),
                (1.5, 0),
                (0.5, 0.25),
                (0.5, 0,),
            ]

            draw_points(points,
                        vertices_show=True,
                        labels=[
                            ("O", (-0.1, -0.2)),
                            # ("$P(y, z)$", (-0.3, 0.1)),
                            ("$P$", (-0.05, 0.1)),
                            ('$-z$', (-0.05, -0.2)),
                            # ("$S(y',d)$", (-0.35, 0.1)),
                            ("$S$", (-0.15, 0.05)),
                            ("$-d$", (-0.05, -0.2)),
                        ],  # Підписи вершин
                        vertex_color="red",
                        )
            print_label(start=(0.25, 0.8),
                        label=r"$screen$",
                        # label_color="green",
                        # label_fontsize=13,
                        # label_offset=(-0.2, 0.1)
                        )

    O = np.array([0, 0])
    x = Vec3(1, 0)
    y = Vec3(0, 1)

    scene = Scene(
        title="",
        coordinate_rect=(-1, -1, 2.5, 2),
        grid_show=False,
        base_axis_show=False,
        axis_show=False,
        axis_color=("brown", "brown"),
        axis_line_style="-."
    )

    line = LineModel(0,0, 2, 1, color="brown", linewidth=1.5)


    Oz = Axis(0, 0, 2, 0, color="blue", linewidth=1.5, line_style="--",
              label="$-Z$", label_offset=(0.1, 0.1))
    Oy = Axis(0, -0, 0, 1.2, color="grey", linewidth=1.5, line_style="--",
              label="$Y$", label_offset=(0.1, 0.05))
    screen = LineModel(0.5, -0.1, 0.5, 0.7, color="green", linewidth=3., line_style="--", )
    y2 = LineModel(1.5, 0, 1.5, 0.75, color="black", linewidth=1., line_style="--", )

    scene["OZ_ID"] = Oz
    scene["oy"] = Oy
    scene["y1"] = screen
    scene["y2"] = y2
    scene["line"] = line

    scene.add_frames(frame1)
    scene.show()
