import numpy as np
from typing import TextIO
from ..._openerinterface import OpenerInterface


WIDTH = [5, 5, 5, 5, 8, 8, 8, 8, 8, 8]
COLMUN = ["resnum", "resname", "atom", "id", "x", "y", "z", "vx", "vy", "vz"]


class GROOpener(OpenerInterface):
    fmt = "gro"
    _numb_additional_lines = 3
    __is_update_column = False

    def __init__(self, cls) -> None:
        super().__init__(cls)
        self._width = WIDTH
        self.update_columns(COLMUN)

    def _extract_snapshot(self, firstline: str, file: TextIO) -> list:
        natom = int(file.readline().strip())
        data = np.genfromtxt(file, delimiter=self._width, dtype=str, max_rows=natom)
        box = np.diag(file.readline().split())
        self.update_box(box=box)
        self.update_natoms(natoms=natom)
        data = self.__check_data(data=data)
        return data

    def __check_data(self, data):
        if not self.__is_update_column:
            if "\n" in data[0]:
                self._width = self._width[:6]
                data = data[:, :6]
                self.update_columns(COLMUN[:6])
            self.__is_update_column = True
        return data
