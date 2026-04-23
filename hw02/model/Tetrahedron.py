from src.engine.model.Model import Model
from src.engine.model.SimplePolygon import SimplePolygon


class Tetrahedron(Model):
    def __init__(self, vertices=None, alpha=1.0, color="cyan", edge_color="blue",
                 line_style="-", line_width=1.0):
        super().__init__()
        if vertices is None:
            vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
        faces = [[vertices[j] for j in idx]
                 for idx in ([0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3])]
        self.polygons = [
            SimplePolygon(*face, color=color, edgecolor=edge_color, alpha=alpha,
                          line_width=line_width, line_style=line_style)
            for face in faces
        ]

    def draw_model(self, plt_axis):
        for p in self.polygons:
            p.transformation = self.transformation
            p.pivot(self._pivot)
            p.draw(plt_axis)

    def apply_transformation_to_geometry(self):
        super().apply_transformation_to_geometry()
        for p in self.polygons:
            p.apply_transformation_to_geometry()