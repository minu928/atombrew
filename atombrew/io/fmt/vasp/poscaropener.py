import numpy as np
from typing import TextIO
from ..._openerinterface import OpenerInterface


class POSCAROpener(OpenerInterface):
    fmt = "poscar"
    _numb_additional_lines = 8

    def __init__(self, cls) -> None:
        super().__init__(cls)
        self.update_columns(np.array(["atom", "x", "y", "z"]))

    def _extract_snapshot(self, firstline: str, file: TextIO) -> list:
        SCALE = float(file.readline())
        box = np.loadtxt(file, max_rows=3, dtype=float) * SCALE
        self.update_box(box=box)
        kind_atoms = file.readline().split()
        numb_atoms = np.array(file.readline().split(), dtype=int)
        atoms = np.repeat(kind_atoms, numb_atoms)
        natoms = len(atoms)
        self.update_natoms(natoms=natoms)
        type_xyz = file.readline().strip()
        assert type_xyz == "Cartesian"
        xyz_lines = np.loadtxt(file, max_rows=natoms, dtype=str)
        return np.c_[atoms, xyz_lines]
