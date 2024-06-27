import numpy as np
from tqdm import tqdm
from ._openerinterface import openers


class Opener(object):
    supporting_fmt = tuple(openers.keys())
    frame = 0
    natoms = 0
    _box = []
    _columns = []

    def __init__(self, filename: str, *, fmt: str = "auto") -> None:
        self._filename = filename
        self._fmt = self._set_format(fmt=fmt)
        self._fmt_opener = openers[self._fmt](cls=self)
        self.reset()
        self.nextframe()

    @property
    def database(self):
        return self._database

    @property
    def data(self) -> np.ndarray:
        return self._data

    @property
    def box(self):
        return np.array(self._box)

    @property
    def columns(self):
        return np.array(self._columns)

    @property
    def keys(self):
        return {"atom": self._fmt_opener._atom_keyword}

    def load_database(self):
        with open(file=self._filename, mode="r") as file:
            for _ in range(self._fmt_opener.skip_headline_num):
                next(file)
            while True:
                try:
                    yield np.array(self._fmt_opener.extract_snapshot(file=file))
                except StopIteration:
                    break
                except Exception as e:
                    raise AssertionError(f"Unexpected error: {e}")

    def _set_format(self, fmt: str):
        if fmt == "auto":
            fmt = self._filename.split(".")[-1]
        assert fmt in self.supporting_fmt, f"Not Supporting Format({fmt}), We support ({self.supporting_fmt})"
        return fmt

    def reset(self):
        self.frame, self.natoms, self._box = -1, None, []
        self._database = self.load_database()

    def nextframe(self):
        self._data = next(self.database)

    def moveframe(self, frame: int):
        self.reset()
        for _ in range(frame):
            self.nextframe()

    def frange(self, start: int = 0, end: int = None, step: int = 1, *, verbose: bool = True):
        assert end is None or start < end, "start should be lower than end"
        bar = tqdm(unit=" frame")
        self.moveframe(start)
        try:
            while self.frame != end:
                self.nextframe()
                if (self.frame - start) % step == 0:
                    if verbose:
                        bar.update(1)
                    yield self.frame
        except StopIteration:
            pass
        except Exception as e:
            raise AssertionError(f"Unexpected error: {e}")
        finally:
            self.reset()
