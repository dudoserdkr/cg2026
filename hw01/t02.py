from utils import (
    get_vertices,
    get_rectanglescene,
    get_homogeneous_vertices,
    get_rotation_matrix,
    get_scale,
    print_current_transformation,
)


FILE_NAME = "assets/t02.md"


def frame1(scene):
    rect_vertices = get_vertices()
    rect = scene["rect"]
    rect["color"] = "blue"
    rect.set_geometry(rect_vertices.flatten())
    print_current_transformation(vertices=rect_vertices, frame_number=1, step_number=1, file_name=FILE_NAME)

def frame2(scene):
    vertices_h = get_homogeneous_vertices() # vertices_h stands for homogeneous vertices
    S = get_scale(2, 2)
    vertices_h = (S @ vertices_h.T).T
    print_current_transformation(S=S, vertices=vertices_h, step_number=1, frame_number=2, file_name=FILE_NAME)
    R = get_rotation_matrix(45)
    vertices_h = (R @ vertices_h.T).T
    print_current_transformation(R=R, S=S, vertices=vertices_h, step_number=2, frame_number=2, file_name=FILE_NAME)

    rect = scene["rect"]
    rect.set_geometry(vertices_h[:, :2].flatten())
    rect["color"] = "red"




if __name__ == '__main__':

    scene = get_rectanglescene()
    scene.add_frames(frame1)
    scene.add_frames(frame2)
    scene.show()