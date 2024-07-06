import numpy as np
from numpy.typing import ArrayLike


def apply_pbc(vec, box):
    box = np.array(box, dtype=float)
    vec = np.array(vec, dtype=float)
    half_box = box * 0.5
    return (vec + half_box) % box - half_box


def wrap(coords, box):
    box = np.array(box, dtype=float)
    coords = np.array(coords, dtype=float)
    return np.mod(coords, box)


def unwrap(coords, box):
    coords = np.array(coords, dtype=float)
    assert coords.ndim == 3, f"coords ndim != 3, your ndim: {coords.ndim}"
    box = np.array(box, dtype=float)
    assert box.ndim == 3, f"box ndim != 3, your ndim: {box.ndim}"
    unwrapped_xyz = np.copy(coords)
    for i in range(1, coords.shape[0]):
        ibox = np.diag(box[i])
        delta = coords[i] - coords[i - 1]
        delta -= np.round(delta / ibox) * ibox
        unwrapped_xyz[i] = unwrapped_xyz[i - 1] + delta
    return unwrapped_xyz
