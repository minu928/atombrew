from typing import IO
from abc import ABCMeta, abstractmethod


class WriterInterface(metaclass=ABCMeta):
    def __init__(self, file: IO) -> None:
        self.file = file

    def __init_subclass__(cls) -> None:
        writers[cls.fmt] = cls

    @property
    @abstractmethod
    def fmt(self) -> str:
        pass

    @abstractmethod
    def write(self, atoms, coords, *, box=None, force=None, **kwrgs):
        pass


writers: dict[str, type[WriterInterface]] = {}
