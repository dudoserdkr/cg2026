from hw02.Frame import Frame
from hw02.utils import get_cube_scene, get_cube_vertices
from hw02.constants import *

FILE_NAME = "assets/t01.md"


def frame1(scene):
    (Frame(scene, "cube", get_cube_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "cube", get_cube_vertices, 2, FILE_NAME).
     scale([2, 0.5, 1]).
     finish(FRAME_2))


def frame3(scene):
    (Frame(scene, "cube", get_cube_vertices, 3, FILE_NAME).
     scale([2, 0.5, 1]).
     euler_rotate("XYZ", [30, 45, 60]).
     finish(FRAME_3))


def frame4(scene):
    (Frame(scene, "cube", get_cube_vertices, 4, FILE_NAME).
     scale([2, 0.5, 1]).
     euler_rotate("XYZ", [30, 45, 60]).
     translate([-3, 2, 5]).
     finish(FRAME_4))


if __name__ == '__main__':
    scene = get_cube_scene()
    scene.add_frames(frame1, frame2, frame3, frame4)
    scene.show()
