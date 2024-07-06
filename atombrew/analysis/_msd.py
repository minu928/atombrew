import numpy as np
from tqdm import trange
from atombrew.space import unwrap


# Class of Mean Square Displacement
class MSD(object):
    axis_dict = {"frame": 0, "natoms": 1, "dim": -1}

    def __init__(self, position, *, fft: bool = True, dtype: str = float):
        self.dtype = str(dtype)
        self.fft = bool(fft)
        self.position = np.array(position, dtype=self.dtype)
        self.nframe = self.position.shape[0]

    def run(self, start: int = 0, stop: int = None, step: int = 1):
        if self.fft:
            self._result = self._calc_msd_with_fft()
        else:
            self._result = self._calc_msd_with_window()
        return self

    @property
    def result(self):
        if not hasattr(self, "_result"):
            self.run()
        return self._result

    def _calc_msd_with_window(self):
        msd_list = np.zeros(self.position.shape[:2])
        for frame in trange(1, self.nframe, unit="frame"):
            distance = self.__square_sum_position(self.position[frame:] - self.position[:-frame])
            msd_list[frame, :] = np.mean(distance, axis=self.axis_dict["frame"])
        return self.__mean_msd_list(msd_list=msd_list)

    def _calc_msd_with_fft(self):
        S_1 = self._calc_S1()
        S_2 = self._calc_S2()
        msd_list = np.subtract(S_1, 2.0 * S_2)
        return msd_list.mean(axis=self.axis_dict["natoms"])

    def _calc_S1(self):
        empty_matrix = np.zeros(self.position.shape[:2])
        D = np.square(self.position).sum(axis=self.axis_dict["dim"])
        D = np.append(D, empty_matrix, axis=self.axis_dict["frame"])
        Q = 2.0 * np.sum(D, axis=self.axis_dict["frame"])
        S_1 = empty_matrix
        for m in trange(self.nframe, unit="frame"):
            Q -= D[m - 1, :] + D[self.nframe - m, :]
            S_1[m, :] = Q / (self.nframe - m)
        return S_1

    def _calc_S2(self):
        X = np.fft.fft(self.position, n=2 * self.nframe, axis=self.axis_dict["frame"])
        dot_X = X * X.conjugate()
        x = np.fft.ifft(dot_X, axis=self.axis_dict["frame"])
        x = x[: self.nframe].real
        x = x.sum(axis=self.axis_dict["dim"])
        n = np.arange(self.nframe, 0, -1)
        return x / n[:, np.newaxis]
