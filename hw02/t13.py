from Frame import Frame
from hw02.utils import get_tetrahedron_scene, get_tetrahedron_vertices
from constants import *

FILE_NAME = "assets/t13.md"


def frame1(scene):
    (Frame(scene, "tetra", get_tetrahedron_vertices, 1, FILE_NAME).
     finish(FRAME_1))


def frame2(scene):
    (Frame(scene, "tetra", get_tetrahedron_vertices, 2, FILE_NAME, local=True).
     rotate([1, 0, 0], 45).
     finish(FRAME_2))


def frame3(scene):
    (Frame(scene, "tetra", get_tetrahedron_vertices, 3, FILE_NAME, local=True).
     rotate([1, 0, 0], 45).
     translate([0, 2, 0]).
     finish(FRAME_3))


def frame4(scene):
    (Frame(scene, "tetra", get_tetrahedron_vertices, 4, FILE_NAME, local=True).
     rotate([1, 0, 0], 45).
     translate([0, 2, 0]).
     rotate([0, 0, 1], 30).
     finish(FRAME_4))


if __name__ == '__main__':
    scene = get_tetrahedron_scene()
    scene.add_frames(frame1, frame2, frame3, frame4)
    scene.show()