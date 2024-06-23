from collections import defaultdict
from scipy.constants import Avogadro
from ._mass import change_element_to_mass
from ._arithmeticable import Arithmeticalble


class Molecule(Arithmeticalble):
    def __init__(self, elements: str) -> None:
        self._elements = elements
        self._element_info = self.__check_elements(elements)
        self._mw = self.__calc_mw()
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

    def __check_elements(self, elements: str) -> dict[str, int]:
        element_dict = defaultdict(int)
        tmp_element = ""
        for char in elements:
            if char.isupper():
                if tmp_element:
                    element_dict[tmp_element] += 1
                    tmp_element = ""
            elif char.isnumeric():
                element_dict[tmp_element] += int(char)
                tmp_element = ""
                continue
            tmp_element += char
        if tmp_element:
            element_dict[tmp_element] += 1
        return element_dict

    def __calc_mw(self):
        mw = 0.0
        for element, num in self._element_info.items():
            mw += change_element_to_mass(element=element) * num
        return mw
