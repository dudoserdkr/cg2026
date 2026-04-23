from Frame import Frame
from hw02.utils import get_rectangle_vertices, get_rectangle_scene
from constants import *

FILE_NAME = "assets/t09.md"


def frame1(scene):
    (Frame(scene, "rect", get_rectangle_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "rect", get_rectangle_vertices, 2, FILE_NAME).
     rotate_around_pivot([0, 1, 0], 60, [3, 3, 0]).
     finish(FRAME_2))


def frame3(scene):
    (Frame(scene, "rect", get_rectangle_vertices, 3, FILE_NAME).
     rotate_around_pivot([0, 1, 0], 60, [3, 3, 0]).
     rotate_around_pivot([1, 0, 0], 30, [3, 3, 0]).
     finish(FRAME_3))


if __name__ == '__main__':
    scene = get_rectangle_scene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.add_frames(frame3)
    scene.show()