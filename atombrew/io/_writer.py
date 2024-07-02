import os
from ._writerinterface import writers


class Writer(object):
    supporting_fmt = tuple(writers.keys())

    def __init__(self, filename: str, mode="w", *, fmt: str = "auto") -> None:
        assert mode == "w+" or not os.path.isfile(filename), FileExistsError("Already File Exits")
        self._filename = filename
        self._mode = mode
        self.fmt = self._set_format(fmt=fmt)
        self._fmt_writer = writers[self.fmt]

    def __enter__(self):
        self.file = open(self._filename, mode=self._mode)
        return self._fmt_writer(self.file)

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

    def _set_format(self, fmt: str):
        fmt = fmt.lower()
        if fmt == "auto":
            fmt = self._filename.split(".")[-1]
        assert fmt in self.supporting_fmt, f"Not Supporting Format({fmt}), We support {self.supporting_fmt}"
        return fmt
