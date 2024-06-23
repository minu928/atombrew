class Opener(object):
    def __init__(self, filename: str, fmt: str = "auto") -> None:
        self._filename = filename
        self._fmt = self.__check_fmt(fmt=fmt)

    def open(self):
        with open(file=self._filename, mode="r") as f:
            while True:
                try:
                    pass
                except StopIteration:
                    break
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    break

    def __check_fmt(self, fmt: str) -> str:
        fmt = self._filename.split(".")[-1]
        return fmt
