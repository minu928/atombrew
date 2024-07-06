import numpy as np
from typing import Union
from .io import TRJOpener, TRJWriter


class Home(TRJOpener):
    def __init__(self, filename: str, *, fmt: str = "auto") -> None:
        super().__init__(filename, fmt=fmt)

    @property
    def atoms(self) -> np.ndarray:
        if not hasattr(self, "_atom_id"):
            self._atom_id = self.find_index(what=self.keys.get("atom"))
        return np.char.strip(self.data[:, self._atom_id])

    @property
    def coords(self) -> np.ndarray:
        if not hasattr(self, "_xyz_id"):
            self._xyz_id = self.find_index(what=["x", "y", "z"])
        return self.data[:, self._xyz_id].astype(float)

    @property
    def velocities(self) -> np.ndarray:
        if not hasattr(self, "_vxyz_id"):
            self._vxyz_id = self.find_index(what=["vx", "vy", "vz"])
        return self.data[:, self._vxyz_id].astype(float)

    @property
    def forces(self) -> np.ndarray:
        if not hasattr(self, "_fxyz_id"):
            self._fxyz_id = self.find_index(what=["fx", "fy", "fz"])
        return self.data[:, self._fxyz_id].astype(float)

    def find_index(self, what: Union[list[str], str]):
        return np.where(np.isin(self.columns, what))[0]

    def find_atom(self, atom: str):
        return np.where(np.char.startswith(self.atoms, atom))[0]

    def brew(self, what: Union[list[str], str] = None, atom: str = None):
        atom_indices = self.find_atom(atom) if atom is not None else slice(None)
        col_indices = self.find_index(what) if what is not None else slice(None)
        if isinstance(atom_indices, np.ndarray) and isinstance(col_indices, np.ndarray):
            return self.data[np.ix_(atom_indices, col_indices)]
        return self.data[atom_indices, col_indices]

    def write(
        self,
        filename: str,
        mode: str = "w",
        start: int = 0,
        stop: int = None,
        step: int = 1,
        *,
        fmt: str = "auto",
        verbose: bool = True,
        **kwrgs
    ):
        with TRJWriter(filename=filename, mode=mode, fmt=fmt) as f:
            for _ in self.frange(start=start, stop=stop, step=step, verbose=verbose):
                f.write(
                    atoms=self.atoms,
                    coords=self.coords,
                    box=self.box,
                    forces=self.forces,
                    velocities=self.velocities,
                    **kwrgs,
                )
