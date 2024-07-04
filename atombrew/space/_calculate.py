import numpy as np


def calc_distance(vec, axis: int = -1, dtype: str = float):
    return np.sqrt(np.sum(np.square(vec), axis=axis)).astype(dtype)


def calc_angle(v1, v2):
    dot_product = np.sum(v1 * v2, axis=-1)
    norm_v1 = np.linalg.norm(v1, axis=-1)
    norm_v2 = np.linalg.norm(v2, axis=-1)
    return np.arccos(dot_product / (norm_v1 * norm_v2)) * 180.0 / np.pi
