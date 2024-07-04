import numpy as np


def apply_pbc(vec, box):
    box = np.array(box, dtype=float)
    vec = np.array(vec, dtype=float)
    half_box = box * 0.5
    return (vec + half_box) % box - half_box


def wrap(coords, box):
    box = np.array(box, dtype=float)
    coords = np.array(coords, dtype=float)
    return np.mod(coords, box)
