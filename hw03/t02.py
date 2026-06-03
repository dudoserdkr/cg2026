from hw02.Frame import Frame
from hw02.utils import get_cube_scene, get_cube_vertices
from hw02.constants import *

FILE_NAME = "assets/t02.md"


def frame1(scene):
    (Frame(scene, "cube", get_cube_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "cube", get_cube_vertices, 2, FILE_NAME).
     euler_rotate("ZYX", [20, 35, 50]).
     finish(FRAME_2))


def frame3(scene):
    (Frame(scene, "cube", get_cube_vertices, 3, FILE_NAME).
     euler_rotate("ZYX", [20, 35, 50]).
     translate([1, 3, -2]).
     finish(FRAME_3))


if __name__ == '__main__':
    scene = get_cube_scene()
    scene.add_frames(frame1, frame2, frame3)
    scene.show()
