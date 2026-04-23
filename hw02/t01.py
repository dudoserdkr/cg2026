from Frame import Frame
from hw02.utils import get_cube_scene, get_cube_vertices

FILE_NAME = "assets/t01.md"

def frame1(scene):
    Frame(scene, "cube", get_cube_vertices, 1, FILE_NAME).finish("blue")

def frame2(scene):
    Frame(scene, "cube", get_cube_vertices, 2, FILE_NAME).rotate([1, 1, 0], 45).finish("red")

def frame3(scene):
    Frame(scene, "cube", get_cube_vertices, 3, FILE_NAME).rotate([1, 1, 0], 45).translate([2, -1, 3]).finish("cyan")


if __name__ == '__main__':
    scene = get_cube_scene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.add_frames(frame3)
    scene.show()