from ._openerinterface import openers


class Opener(object):
    supporting_fmt = tuple(openers.keys())
    frame = 0
    natoms = 0
    box = []
    columns = []

    def __init__(self, filename: str, *, fmt: str = "auto") -> None:
        self._filename = filename
        self._fmt = self._set_format(fmt=fmt)
        self._fmt_opener = openers[self._fmt](cls=self)
        self.reset()

    @property
    def database(self):
        return self._database

    @property
    def data(self):
        return self._current_data

    def load_database(self):
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

    def reset(self):
        self.frame, self.natoms, self.box = -1, None, []
        self._database = self.load_database()
        self.nextframe()

    def nextframe(self):
        self._current_data = next(self.database)

    def _set_format(self, fmt: str):
        if fmt == "auto":
            fmt = self._filename.split(".")[-1]
        assert fmt in self.supporting_fmt, f"Not Supporting Format({fmt}), We support ({self.supporting_fmt})"
        return fmt
