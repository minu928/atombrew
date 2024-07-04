import numpy as np
from atombrew.space import calc_distance, apply_pbc
from abc import ABCMeta, abstractmethod


class RDFInterface(metaclass=ABCMeta):
    def __init__(
        self,
        box=None,
        r_max: float = None,
        resolution: int = 1000,
        dtype: str = float,
    ):
        self.nframe = 0
        self._dtype = dtype
        self.resolution = resolution
        self.r_max = np.max(box) * 0.5 if r_max is None else r_max
        self._histogram = np.zeros(self.resolution)
        self._rdf = np.zeros(self.resolution)

    def __repr__(self) -> str:
        return f"RDF{self.__class__.__name__}"

    @property
    def radii(self):
        if not hasattr(self, "_radii"):
            self._radii = np.linspace(0, self.r_max, num=self.resolution + 1)[:-1]
        return self._radii

    @property
    def result(self):
        if not hasattr(self, "_result"):
            self._result = self._cal_rdf()
        return self._result

    @property
    def cn(self):
        if not hasattr(self, "_cn"):
            self._cn = self._cal_cn()
        return self._cn

    @property
    @abstractmethod
    def n_a(self) -> int:
        pass

    @property
    @abstractmethod
    def n_b(self) -> int:
        pass

    @abstractmethod
    def run(self, start=0, end=None, step=1):
        pass

    def _update_hist(self, a_unit, b_unit, box_unit):
        vec = apply_pbc(a_unit[:, None, :] - b_unit[None, :, :], box=box_unit)
        distance = calc_distance(vec=vec)
        each_hist, _ = np.histogram(distance, bins=self.resolution, range=(0, self.r_max))
        self.nframe += 1
        self._histogram[1:] += each_hist[1:]
        self._rdf[1:] += each_hist[1:] / np.square(self.radii[1:]) * np.prod(box_unit)

    # Calculate the Density Function
    def _cal_rdf(self):
        dr = self.r_max / (self.resolution + 1)
        factor = 4.0 * np.pi * dr * self.nframe * self.n_a * self.n_b
        return self._rdf / factor

    # Function for get coordinate number
    def _cal_cn(self):
        return np.cumsum(self._histogram / (self.nframe * self.n_a))
