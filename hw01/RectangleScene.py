import numpy as np
from src.engine.model.Polygon import Polygon
from src.engine.scene.Scene import Scene


class RectangleScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        polygon = Polygon()
        self["rect"] = polygon
