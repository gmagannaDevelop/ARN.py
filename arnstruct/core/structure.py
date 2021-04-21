from typing import List, Dict, Union, Set, Optional, NoReturn, Any, Callable, Type


class Structure(object):
    """
    Define a
    """

    __Character: Set[str] = set("(-)")

    __complements: Dict[str, str] = {"(": ")", ")" : "(", "-" : "-"}

    def is_valid_structure(struct: str) -> bool:
        """ Determine if input `struct` is a valid ARN structure """
        return set(struct).issubset(Structure.__Character)

    def __init__(self, struct: str):
        """Initialise a ARN sequence from a string,
        verifying that all letters from the string
        are valid ARN bases (A, U, C, G)"""
        if not Structure.is_valid_structure(struct):
            raise ValueError(
                f"Entry sequence contains invalid characters. Valid character is {Structure.__Character}"
            )
        else:
            self._struct: str = struct

    @property
    def structure(self):
        return self._struct

    def __iter__(self):
        return iter(self._struct)

    def motif_search_struct(self, other, th):
        """Search for common motifs between the two ARN and store them in a list"""
        if isinstance(other, Structure):
            other = other.structure
        elif not isinstance(other, str):
            raise TypeError(
                f"argument other is of type {type(other)}. Please provide a string or Sequence"
            )
        l_s_motif=[]

        for i in range(len(self._struct)):
            if self._struct[i:i+th] in other and len(self._struct[i:i+th]) == th:
                l_s_motif.append(self._struct[i:i+th])

        return l_s_motif
