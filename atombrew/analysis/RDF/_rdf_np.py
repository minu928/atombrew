import numpy as np
from tqdm import trange
from ._rdfinterface import RDFInterface


class ByNumpy(RDFInterface):
    def __init__(self, a, b, box=None, r_max: float = None, resolution: int = 1000, dtype: str = ...):
        assert len(a) == len(b), f"Not equal frame of a({len(a)}) and b({len(b)})"
        self.a = np.array(a, dtype=float)
        self.b = np.array(b, dtype=float)
        self.box = self.__check_box(box=box)
        super().__init__(box, r_max, resolution, dtype)

    @property
    def n_a(self):
        if not hasattr(self, "_n_a"):
            self._n_a = self.a.shape[1]
        return self._n_a

    @property
    def n_b(self):
        if not hasattr(self, "_n_b"):
            self._n_b = self.a.shape[1]
        return self._n_b

    def run(self, start=0, stop=None, step=1):
        stop = len(self.a) if stop is None else stop
        for frame in trange(start, stop, step, unit="frame"):
            unit_a = self.a[frame, ...]
            unit_b = self.b[frame, ...]
            unit_box = self.box[frame, ...]
            self._update_hist(unit_a, unit_b, unit_box)
        return self

    def __check_box(self, box):
        assert box is not None, "Please Input Box"
        box = np.array(box, dtype=float)
        if box.ndim == 3 and box.shape[1:] == (3,3):
            return np.array([np.diag(b) for b in box])
        elif box.ndim == 2:
            return box
        elif box.ndim == 1 and len(box) == 3:
            return np.tile(box, [len(self.a), 1])
        else:
            raise ValueError(f"Box should be in shape, (nframe, 3, 3), (nframe, 3), (3,)")