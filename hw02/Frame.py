import numpy as np
from hw02.utils import get_cube_vertices, print_current_transformation, get_scale, get_rotation, get_translation, \
    set_obj_color, get_euler_rotation, get_scale_around_pivot, get_rotation_around_pivot


class Frame:
    def __init__(self, scene, obj_name, get_obj_vert, frame_number, file_name, local=False):
        self.scene = scene

        self.obj_name = obj_name
        self.original = get_obj_vert()
        self.vertices = self.original.copy()

        self.frame_number = frame_number
        self.file_name = file_name

        self.TRS = np.eye(4, dtype=np.float64)
        self.local = local

        self.step = 0

    def apply(self, M, local=None):
        return self._apply(M, local)

    def _apply(self, M, local=None):
        local = self.local if local is None else local
        self.TRS = self.TRS @ M if local else M @ self.TRS
        self.vertices = (self.TRS @ self.original.T).T
        self.step += 1
        print_current_transformation(
            M_step=M, M_total=self.TRS, vertices=self.vertices,
            step_number=self.step, frame_number=self.frame_number,
            file_name=self.file_name,
        )
        return self

    def translate(self, t, local=None):                             return self._apply(get_translation(t), local)
    def rotate(self, axis, angle, local=None):                      return self._apply(get_rotation(axis, angle), local)
    def scale(self, s, local=None):                                 return self._apply(get_scale(s), local)
    def euler_rotate(self, convention, angles, local=None):         return self._apply(get_euler_rotation(convention, angles), local)
    def rotate_around_pivot(self, axis, angle, pivot, local=None):  return self._apply(get_rotation_around_pivot(axis, angle, pivot), local)
    def scale_around_pivot(self, s, pivot, local=None):             return self._apply(get_scale_around_pivot(s, pivot), local)

    def finish(self, color):
        obj = self.scene[self.obj_name]
        set_obj_color(obj, color, color)
        obj.transformation = self.TRS
