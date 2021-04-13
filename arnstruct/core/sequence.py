from typing import (
    List,
    Dict,
    Union,
    Set,
    Optional,
    NoReturn,
    Any,
    Callable,
    Type,
    Tuple,
)

# TODO : check how to implement typehint for self
class Sequence(object):
    """
    Define a
    """

    __Alphabet: Set[str] = set("AUGC")

    __complements: Dict[str, str] = {"A": "U", "U": "A", "C": "G", "G": "C"}

    @staticmethod
    def is_valid_sequence(seq: str) -> bool:
        """ Determine if input `seq` is a valid ARN sequence """
        return set(seq.upper()).issubset(Sequence.__Alphabet)

    def __init__(self, sequence: str):
        """Initialise a ARN sequence from a string,
        verifying that all letters from the string
        are valid ARN bases (A, U, C, G)"""
        if not Sequence.is_valid_sequence(sequence):
            raise ValueError(
                f"Entry sequence contains invalid characters. Valid alphabet is {Sequence.__Alphabet}"
            )
        else:
            self._sequence: str = sequence.upper()

    def __complement(self, letter: str) -> str:
        """ Private method, do not call. Return the complement of a single base. """
        return Sequence.__complements[letter]

    def complement(self, other: Optional[str] = None):
        """
        Return the complement of a Sequence.

        The complements are :
            A <-> U
            C <-> G

        Which are the standard bases for RNA molecules.

        The behaviour is as follows :

        >>> a_sequence.complement()

            returns the complement of self (a_sequence).

        >>> a_sequence.complement(other)

            returns the complement of other.
                * a string if type(other) == str
                * a Sequence if type(other) == Sequence
        """
        if other is None:  # default behaviour : return complement of self
            return Sequence("".join(self.__complement(base) for base in self._sequence))
        elif isinstance(other, str):  # complement of a string, if valid
            if Sequence.is_valid_sequence(other):
                return "".join(self.__complement(base) for base in other)
            else:
                raise ValueError(
                    f"Sequence contains invalid characters. Valid characters are {Sequence.__Alphabet}"
                )
        elif isinstance(other, Sequence):  # complement of other Sequence object
            return other.complement()
        else:
            raise TypeError(
                f"Complement of {type(other)} object is undefined. Please provide a Sequence or string"
            )

    @property
    def sequence(self):
        return self._sequence

    # TODO : show only part of the sequence
    def __repr__(self):
        return f"ARN Sequence({self.sequence})"

    def __str__(self):
        return self.sequence

    def __len__(self):
        return len(self.sequence)

    def __iter__(self):
        return iter(self.sequence)

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            raise TypeError(f"Cannot compare Sequence to object of class {type(other)}")

        return self._sequence == other._sequence

    def motif_search(self, other: str, th: int, unique: bool = False) -> List[str]:
        """Search for common motifs between the two ARN and store them in a list"""
        if isinstance(other, Sequence):
            other = other.sequence
        elif not isinstance(other, str):
            raise TypeError(
                f"argument other is of type {type(other)}. Please provide a string or Sequence"
            )

        l_motif: List[str] = []

        for i in range(len(self._sequence) - th):
            if self._sequence[i : i + th] in other:
                l_motif.append(self._sequence[i : i + th])

        if unique:
            l_motif = list(set(l_motif))

        return l_motif
