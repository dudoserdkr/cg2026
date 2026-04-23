import numpy as np
from Frame import Frame
from hw02.utils import get_cube_scene, get_cube_vertices, get_tetrahedron_vertices, get_tetrahedron_scene
from constants import *

FILE_NAME = "assets/t05.md"


rng = np.random.default_rng(seed=42)
angle = rng.uniform(10, 90)
axis = rng.uniform(-1, 1, size=3)
t = rng.uniform(-5, 5, size=3)


def frame1(scene):
    (Frame(scene, "tetra", get_tetrahedron_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "tetra", get_tetrahedron_vertices, 1, FILE_NAME).
     rotate(axis, angle).
     finish(FRAME_2))

def frame3(scene):
    (Frame(scene, "tetra", get_tetrahedron_vertices, 1, FILE_NAME).
     rotate(axis, angle).translate(t).
     finish(FRAME_3))


if __name__ == '__main__':
    scene = get_tetrahedron_scene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.add_frames(frame3)
    scene.show()