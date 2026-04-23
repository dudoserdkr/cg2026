from src.engine.model.Cube import Cube
from src.engine.scene.Scene import Scene


class CubeScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cube = Cube(alpha=0.3, color="cyan", edge_color="blue")
        self["cube"] = cube
