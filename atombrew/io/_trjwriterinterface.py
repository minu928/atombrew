from typing import IO
from abc import ABCMeta, abstractmethod


class TRJWriterInterface(metaclass=ABCMeta):
    def __init__(self, file: IO) -> None:
        self.file = file

    def __init_subclass__(cls) -> None:
        trj_writers[cls.fmt] = cls

    @property
    @abstractmethod
    def fmt(self) -> str:
        pass

    @abstractmethod
    def write(self, atoms, coords, forces, velocities, *, box=None, **kwrgs):
        pass


trj_writers: dict[str, type[TRJWriterInterface]] = {}
