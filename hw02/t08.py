from Frame import Frame
from hw02.utils import get_triangle_vertices, get_cube_vertices, get_triangle_scene
from constants import *

FILE_NAME = "assets/t08.md"


def frame1(scene):
    (Frame(scene, "tri", get_triangle_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "tri", get_triangle_vertices, 2, FILE_NAME).
     rotate_around_pivot([1, 1, 1], 90, [2, 3, 4]).
     finish(FRAME_2))

def frame3(scene):
    (Frame(scene, "tri", get_triangle_vertices, 3, FILE_NAME).
     rotate_around_pivot([1, 1, 1], 90, [2, 3, 4]).
     translate([0, -3, 2]).
     finish(FRAME_3))

if __name__ == '__main__':
    scene = get_triangle_scene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.add_frames(frame3)
    scene.show()