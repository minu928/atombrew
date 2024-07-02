import numpy as np
from typing import TextIO
from ..._openerinterface import OpenerInterface


class LAMMPSTRJOpener(OpenerInterface):
    fmt = "lammpstrj"
    _atom_keyword = "type"
    _numb_additional_lines = 9

    def _extract_snapshot(self, firstline: str, file: TextIO) -> list:
        next(file)
        next(file)
        # * Atom Line
        natoms = int(file.readline().strip())
        self.update_natoms(natoms=natoms)
        # * Box Line
        next(file)
        box = np.diag([sum([float(b) * (-1) ** (i + 1) for i, b in enumerate(file.readline().split())]) for i in range(3)])
        self.update_box(box=box)
        # * Column Line
        columns = file.readline().split()[2:]
        if "element" in columns:
            self._atom_keyword = "element"
        self.update_columns(columns=columns)
        return np.loadtxt(file, max_rows=natoms, dtype=str)
