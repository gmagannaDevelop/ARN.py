import numpy as np
from .sequence import Sequence


class RNAStruct(Sequence):
    """ Calculate secondary structure by dynamic programming """

    def __init__(self, sequence: str):
        super().__init__(sequence)
        # for i in self.sequence:
        #    print(self._Sequence__complement(i))
        n: int = len(self.sequence)
        self._matrix = np.zeros((n, n))

    def _gamma(self, i, j) -> int:
        return (
            1 if self.sequence[i] == self._Sequence__complement(self.sequence[j]) else 0
        )

    def dynamic_prog(self):
        pass
