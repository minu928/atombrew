class Arithmeticalble:
    def __mul__(self, num):
        if not isinstance(num, (int, float)):
            raise TypeError(f"Multiplication requires a number, got {type(num).__name__}")
        self._mw *= num
        self._systeminfo = f"{self._elements}({num})"
        return self

    def __add__(self, other):
        if not isinstance(other, Arithmeticalble):
            raise TypeError(f"Addition requires an instance of Arithmeticalble, got {type(other).__name__}")
        self._mw += other._mw
        self._systeminfo = f"{self._systeminfo}{other._systeminfo}"
        return self
