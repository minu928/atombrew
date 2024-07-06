import numpy as np
from typing import TextIO
from ..._openerinterface import OpenerInterface


PROPERTY_CANDIDATES = {
    "species": ["atom"],
    "atoms": ["atom"],
    "pos": ["x", "y", "z"],
    "positions": ["x", "y", "z"],
    "coords": ["x", "y", "z"],
    "forces": ["fx", "fy", "fz"],
    "vel": ["vx", "vy", "vz"],
    "velocities": ["vx", "vy", "vz"],
}


class EXTXYZOpener(OpenerInterface):
    fmt = "extxyz"
    _numb_additional_lines = 2
    is_update_columns = False

    def __init__(self, cls) -> None:
        super().__init__(cls)

    def _extract_snapshot(self, firstline: str, file: TextIO) -> list:
        natoms = int(firstline.strip())
        self.update_natoms(natoms=natoms)
        self._update_info(secondline=file.readline())
        return np.loadtxt(file, max_rows=natoms, dtype=str)

    def _update_info(self, secondline: str):
        # * Update Box
        box_str = secondline.split('Lattice="')[1].split('"')[0]
        box_str = np.array(box_str.split(), dtype=float).reshape(3, 3)
        self.update_box(box=box_str)
        # * Update Properties
        if not self.is_update_columns:
            properties_str = secondline.split("Properties=")[1].split()[0]
            properties = properties_str.split(":")[0::3]
            columns = []
            for property in properties:
                this_column = PROPERTY_CANDIDATES.get(property, None)
                assert this_column is not None, f"property: {property} is not supported, {tuple(PROPERTY_CANDIDATES.keys())}"
                columns.extend(this_column)
            self.update_columns(columns=columns)
            self.is_update_columns = True
