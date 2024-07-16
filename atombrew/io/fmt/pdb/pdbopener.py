import numpy as np
from typing import TextIO
from ..._trjopenerinterface import TRJOpenerInterface


WIDTH = [6, 5, 1, 4, 1, 4, 1, 4, 1, 3, 8, 8, 8, 6, 6, 10, 2, 2]
COLMUN = np.array(
    [
        "pdbtype",
        "id",
        "_",
        "atom",
        "indicator",
        "resname",
        "chain",
        "resid",
        "rescode",
        "_",
        "x",
        "y",
        "z",
        "occupancy",
        "temp_factor",
        "seg_id",
        "element",
        "charge",
    ]
)


class PDBOpener(TRJOpenerInterface):
    fmt = "pdb"
    _numb_additional_lines = 3
    __natom = None
    __is_update_columns = False

    def __init__(self, cls) -> None:
        super().__init__(cls)
        self._width = WIDTH
        self.skip_headline_num = 2

    def _extract_snapshot(self, firstline: str, file: TextIO) -> list:
        box = np.diag([float(i) for i in file.readline().split()[1:4]])
        self.update_box(box=box)
        if self.__is_update_columns:
            data = np.genfromtxt(
                file,
                delimiter=self._width,
                dtype=str,
                max_rows=self.__natom,
                usecols=self._not_none_cols,
                autostrip=True,
            )
            next(file)
        else:
            start_indices = np.cumsum(np.concatenate(([0], WIDTH[:-1])))
            data = []
            while not (line := file.readline()).startswith("END"):
                idata = [line[start : start + width].strip() for start, width in zip(start_indices, WIDTH)]
                if not self.__is_update_columns:
                    self._not_none_cols = [i for i, cdata in enumerate(idata) if len(cdata)]
                    self.__is_update_columns = True
                    self.update_columns(COLMUN[self._not_none_cols])
                data.append(idata)
            data = np.array(data)[:, self._not_none_cols]
            self.__natom = len(data)
            self.update_natoms(natoms=self.__natom)
        return data
