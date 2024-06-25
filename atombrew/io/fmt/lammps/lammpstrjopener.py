from typing import TextIO
from ..._openerinterface import OpenerInterface


class LAMMPSTRJOpener(OpenerInterface):
    fmt = "lammpstrj"

    def _extract_snapshot(self, firstline: str, file: TextIO) -> list:
        next(file)
        next(file)
        # * Atom Line
        natoms = int(file.readline().strip())
        self.update_natoms(natoms=natoms)
        # * Box Line
        next(file)
        box = [sum([float(b) * (-1) ** (i + 1) for i, b in enumerate(file.readline().split())]) for i in range(3)]
        self.update_box(box=box)
        # * Column Line
        columns = file.readline().split()[2:]
        self.update_columns(columns=columns)
        return [file.readline().split() for _ in range(natoms)]
