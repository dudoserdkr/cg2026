from src.engine.scene.Scene import Scene
from hw02.model.Triangle import Triangle


class TriangleScene(Scene):
    def __init__(self, vertices=None, **kwargs):
        super().__init__(**kwargs)
        self["tri"] = Triangle(vertices=vertices, alpha=0.3,
                               color="cyan", edge_color="blue")