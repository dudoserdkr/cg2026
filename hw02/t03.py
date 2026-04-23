from Frame import Frame
from hw02.utils import get_cube_scene, get_cube_vertices
from constants import *

FILE_NAME = "assets/t03.md"


def frame1(scene):
    (Frame(scene, "cube", get_cube_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "cube", get_cube_vertices, 2, FILE_NAME).
     rotate([0, 0, 1], 60).
     finish(FRAME_2))

def frame3(scene):
    (Frame(scene, "cube", get_cube_vertices, 3, FILE_NAME).
     rotate([0, 0, 1], 60).rotate([1, 1, 1], 45).
     finish(FRAME_3))

def frame4(scene):
    (Frame(scene, "cube", get_cube_vertices, 4, FILE_NAME).
     rotate([0, 0, 1], 60).rotate([1, 1, 1], 45).translate([4, -2, 1]).
     finish(FRAME_4))


if __name__ == '__main__':
    scene = get_cube_scene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.add_frames(frame3)
    scene.add_frames(frame4)
    scene.show()