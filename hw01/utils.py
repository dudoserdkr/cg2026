import numpy as np


def get_vertices():

    return np.array([[0, 0], [0, 1], [1, 1], [1, 0]])


def rotation_matrix_2d(theta):
    return np.array(
        [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ],dtype=np.float64)