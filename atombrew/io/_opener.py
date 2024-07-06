import numpy as np
from tqdm import tqdm
from ._openerinterface import openers


class Opener(object):
    supporting_fmt = tuple(openers.keys())
    frame, natoms = 0, 0
    _box, _columns = [], []

    def __init__(self, filename: str, *, fmt: str = "auto") -> None:
        self._filename = filename
        self._fmt = self._set_format(fmt=fmt)
        self.reset()

    @property
    def fmt(self):
        return self._fmt

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

    def __generate_db(self):
        with open(file=self._filename, mode="r") as file:
            for _ in range(self._fmt_opener.skip_headline_num):
                next(file)
            while True:
                try:
                    yield self._fmt_opener.extract_snapshot(file=file)
                except StopIteration:
                    break
                except Exception as e:
                    raise AssertionError(f"Unexpected error: {e}")

    def _set_format(self, fmt: str):
        fmt = str(fmt).lower()
        if fmt == "auto":
            fmt = self._filename.split(".")[-1]
        assert fmt in self.supporting_fmt, f"Not Supporting Format({fmt}), We support {self.supporting_fmt}"
        return fmt

    def load_db(self):
        self._database = self.__generate_db()

    def reset(self):
        self._fmt_opener = openers[self._fmt](cls=self)
        self.frame, self._box = -1, []
        self.load_db()
        self.nextframe()
        return self

    def nextframe(self):
        self._data = next(self.database)

    def moveframe(self, frame: int):
        assert frame >= 0 and type(frame) == int, f"frame should be positive integer"
        nlines_per_frame = self.natoms + self._fmt_opener._numb_additional_lines
        original_skip_headline_num = self._fmt_opener.skip_headline_num
        self._fmt_opener.skip_headline_num = nlines_per_frame * frame
        self.frame = frame - 1
        self._box = []
        self.load_db()
        self.nextframe()
        self._fmt_opener.skip_headline_num = original_skip_headline_num

    def frange(self, start: int = 0, end: int = None, step: int = 1, *, verbose: bool = True):
        assert end is None or start < end, "start should be lower than end"
        bar = tqdm(unit=" frame")
        self.moveframe(start)
        try:
            while self.frame != end:
                if (self.frame - start) % step == 0:
                    yield self.frame
                self.nextframe()
                if verbose:
                    bar.update(1)
        except StopIteration:
            pass
        except Exception as e:
            raise AssertionError(f"Unexpected error: {e}")
        finally:
            self.reset()
