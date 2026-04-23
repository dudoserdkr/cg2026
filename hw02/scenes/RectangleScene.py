from src.engine.scene.Scene import Scene
from hw02.model.Rectangle import Rectangle


class RectangleScene(Scene):
    def __init__(self, vertices=None, **kwargs):
        super().__init__(**kwargs)
        self["rect"] = Rectangle(vertices=vertices, alpha=0.3,
                                 color="cyan", edge_color="blue")