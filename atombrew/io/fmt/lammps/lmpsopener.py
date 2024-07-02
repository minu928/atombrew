import numpy as np
from typing import TextIO
from ..._openerinterface import OpenerInterface


class LMPSOpener(OpenerInterface):
    fmt = "lmps"
    _atom_keyword = "type"
    _numb_additional_lines = 12

    def __init__(self, cls) -> None:
        super().__init__(cls)
        self.update_columns(["id", self._atom_keyword, "x", "y", "z"])

    def _extract_snapshot(self, firstline: str, file: TextIO) -> list:
        next(file)
        # * Atom Line
        natoms = int(file.readline().split()[0])
        self.update_natoms(natoms=natoms)
        next(file)
        next(file)
        # * Box Line
        box = np.diag([sum([float(b) * (-1) ** (i + 1) for i, b in enumerate(file.readline().split()[:2])]) for _ in range(3)])
        self.update_box(box=box)
        next(file)
        next(file)
        next(file)
        next(file)
        return np.loadtxt(file, max_rows=natoms, dtype=str)
