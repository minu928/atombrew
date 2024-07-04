import numpy as np
from tqdm import trange
from ._rdfinterface import RDFInterface


class ByNumpy(RDFInterface):
    def __init__(self, a, b, box=None, r_max: float = None, resolution: int = 1000, dtype: str = ...):
        self.a = np.array(a, dtype=float)
        self.b = np.array(b, dtype=float)
        self.box = self.__check_box_dim(box=box)
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

    def __check_box_dim(self, box):
        assert box is not None, "Please Input Box"
        box = np.array(box, dtype=float)
        assert np.prod(box), f"Box shape should be (nframe, 3). not {box.shape}"
        nframe_box = len(box)
        nframe_a = len(self.a)
        nframe_b = len(self.b)
        assert nframe_a == nframe_b, "a and b frame must be same."
        if nframe_box == nframe_a:
            return box
        elif box.ndim == 1:
            return np.tile(box, [nframe_a, 1])
        else:
            raise ValueError(f"Box shape is incorrect, (nframe Box : A : B = {nframe_box} : {nframe_a} : {nframe_b})")
