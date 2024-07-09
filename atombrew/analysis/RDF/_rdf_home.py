from numpy import diag, array, tile
from atombrew import Home
from ._rdfinterface import RDFInterface


class ByHome(RDFInterface):
    _not_has_box_fmt = ["xyz"]

    def __init__(self, home: Home, what_a, what_b, box=None, r_max: float = None, resolution: int = 1000, dtype: str = ...):
        self.home = home.reset()
        self.what_a = self.home.find_atom(atom=what_a)
        self.what_b = self.home.find_atom(atom=what_b)
        self._is_box_none = box is None
        self.box = diag(self.home.box) if self._is_box_none else self._make_box(box=box)
        super().__init__(self.box, r_max, resolution, dtype)

    @property
    def n_a(self):
        if not hasattr(self, "_n_a"):
            self._n_a = len(self.what_a)
        return self._n_a

    @property
    def n_b(self):
        if not hasattr(self, "_n_b"):
            self._n_b = len(self.what_b)
        return self._n_b

    def run(self, start=0, stop=None, step=1):
        home = self.home
        what_a = self.what_a
        what_b = self.what_b
        for frame in self.home.frange(start, stop, step):
            coords = home.coords
            box = diag(home.box) if self._is_box_none else self.box[frame]
            self._update_hist(coords[what_a], coords[what_b], box)
        return self

    def _get_box(self, frame):
        pass
    
    def _make_box(self, box):
        box = array(box, dtype=float)
        if box.ndim == 3 and box.shape[1:] == (3,3):
            return array([diag(b) for b in box])
        elif box.ndim == 2:
            return box
        else:
            raise ValueError(f"Box should be in shape, (nframe, 3, 3), (nframe, 3)")