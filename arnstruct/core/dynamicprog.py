import numpy as np
from .sequence import Sequence


class RNAStruct(Sequence):
    """ Calculate secondary structure by dynamic programming """

    def __init__(self, sequence: str):
        super().__init__(sequence)
        self._n = n = len(self.sequence)
        self._matrix = np.zeros((n, n), dtype=int)

    def _delta(self, i, j) -> int:
        """
        Private method, do not call.
        Pair score. Defined as :
        1 if self.sequence[i] is the complement of self.sequence[j]
        0 otherwise
        """
        return (
            1 if self.sequence[i] == self._Sequence__complement(self.sequence[j]) else 0
        )

    def _dynamic_prog(self) -> np.array:
        """Get the self-alignment matrix for the given sequence, using dynamic programming.
        This method's complexity is :
            O(n^2) in space
            O(n^3) in time
        """
        for k in range(1, self._n):
            idx, idy = np.diag_indices_from(self._matrix)
            idy = idx.copy()
            idx += k
            _upr = self._n - k
            _r_len = lambda i, j: len(range(i + 1, j))
            _max_k = (
                lambda i, j: max(
                    self._matrix[i, m] + self._matrix[m + 1, j] for m in range(i + 1, j)
                )
                if _r_len(i, j) > 0
                else 0
            )
            for j, i in zip(idx[:_upr], idy[:_upr]):
                self._matrix[i, j] = max(
                    self._matrix[i + 1, j],
                    self._matrix[i, j - 1],
                    self._matrix[i + 1, j - 1] + self._delta(i, j),
                    _max_k(i, j),
                )

        return self._matrix

    @property
    def max_n_pairs(self) -> int:
        """Return the max number of aligned paris in a secondary structure
        determined by the maximum entry of the dynamic programming matrix
        calculated on the sequence."""
        return self._dynamic_prog().max()