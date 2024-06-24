from scipy.constants import Avogadro
from .tools import count_elements, calc_molecularweights
from ._arithmeticable import Arithmeticalble


class Molecule(Arithmeticalble):
    def __init__(self, elements: str) -> None:
        self._elements = elements
        self._element_info = count_elements(elements)
        self._mw = calc_molecularweights(element_count=self._element_info)
        self._systeminfo = f"{self._elements}(1)"

    def __repr__(self) -> str:
        return self._systeminfo

    @property
    def mw(self) -> float:
        return self._mw

    def calc_volume(self, density: float, *, verbose: bool = True) -> float:
        volume = self.mw / Avogadro / density * 1e24
        if verbose:
            print(f"{density} g/cm3 -> {volume:.5f} ang3")
        return volume
