import numpy as np
from typing import TextIO
from ..._openerinterface import OpenerInterface


class XYZOpener(OpenerInterface):
    fmt = "xyz"
    _numb_additional_lines = 2

    def __init__(self, cls) -> None:
        super().__init__(cls)
        self.update_columns(np.array(["atom", "x", "y", "z"]))

    def _extract_snapshot(self, firstline: str, file: TextIO) -> list:
        next(file)
        natoms = int(firstline.strip())
        self.update_natoms(natoms=natoms)

        return np.loadtxt(file, max_rows=natoms, dtype=str)
