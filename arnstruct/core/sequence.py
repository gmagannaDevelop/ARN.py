from typing import List, Dict, Union, Set, Optional, NoReturn, Any, Callable, Type


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

    # define grammar (allowed operations for objects of class Sequence) :

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            raise TypeError(f"Cannot compare Sequence to object of class {type(other)}")

        return self._sequence == other._sequence


    def motifSearch(self, other, th):
        """Search for common motifs between the two ARN and store them in a list"""
        l_motif=[]

        for i in range(len(self._sequence)-th):
            if self._sequence[i:i+th] in other:
                l_motif.append(self._sequence[i:i+th])

        return l_motif, len(l_motif)


    def count_occurences(self, l_motif):
        """Create a dictionnary with the numbre of occurences of each motif"""
        d_occ={}

        for i in l_motif:
            occ = 0
            for j in l_motif:
                if i == j:
                    occ+=1
                    d_occ.update({i : occ})

        return d_occ





