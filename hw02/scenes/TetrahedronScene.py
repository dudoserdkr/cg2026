from hw02.model import Tetrahedron
from src.engine.scene.Scene import Scene


class TetrahedronScene(Scene):
    def __init__(self, vertices=None, **kwargs):
        super().__init__(**kwargs)
        tetra = Tetrahedron(vertices=vertices, alpha=0.3, color="cyan", edge_color="blue")
        self["tetra"] = tetra