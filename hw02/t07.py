from Frame import Frame
from hw02.utils import get_cube_scene, get_cube_vertices
from constants import *

FILE_NAME = "assets/t07.md"


def frame1(scene):
    (Frame(scene, "cube", get_cube_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "cube", get_cube_vertices, 2, FILE_NAME).
     scale_around_pivot([1, 1, 3], [1, 2, 3]).
     finish(FRAME_2))

def frame3(scene):
    (Frame(scene, "cube", get_cube_vertices, 3, FILE_NAME).
     scale_around_pivot([1, 1, 3], [1, 2, 3]).rotate_around_pivot([0, 0, 1], 30, [1, 2, 3]).
     finish(FRAME_3))


if __name__ == '__main__':
    scene = get_cube_scene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.add_frames(frame3)
    scene.show()