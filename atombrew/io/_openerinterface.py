from typing import TextIO
from abc import ABCMeta, abstractmethod


class OpenerInterface(metaclass=ABCMeta):
    def __init__(self, cls) -> None:
        self.cls = cls
        self.skip_headline_num = 0

    def __init_subclass__(cls) -> None:
        openers[cls.fmt] = cls

    @property
    @abstractmethod
    def fmt(self) -> str:
        pass

    def extract_snapshot(self, file: TextIO) -> list:
        firstline = file.readline()
        if not firstline:
            raise StopIteration()
        self.update_frame()
        return self._extract_snapshot(firstline=firstline, file=file)

    @abstractmethod
    def _extract_snapshot(self, firstline: str, file: TextIO) -> list:
        pass

    def update_frame(self):
        self.cls.frame += 1

    def update_box(self, box):
        self.cls.box = box

    def update_natoms(self, natoms):
        self.cls.natoms = natoms

    def update_columns(self, columns):
        self.cls.columns = columns


openers: dict[str, type[OpenerInterface]] = {}
