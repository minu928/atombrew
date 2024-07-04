from numpy import diag
from atombrew import Home
from ._rdfinterface import RDFInterface


class ByHome(RDFInterface):
    _not_has_box_fmt = ["xyz"]

    def __init__(self, home: Home, what_a, what_b, box=None, r_max: float = None, resolution: int = 1000, dtype: str = ...):
        self.home = home.reset()
        self.what_a = self.home.find_atom(atom=what_a)
        self.what_b = self.home.find_atom(atom=what_b)
        self.box = diag(self.home.box) if box is None else box
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
        for _ in self.home.frange(start, stop, step):
            coords = home.coords
            self._update_hist(coords[what_a], coords[what_b], diag(home.box))
        return self
