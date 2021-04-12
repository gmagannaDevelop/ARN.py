
class Sequence(object):

    Alphabet = set("AUGC")

    def __init__(self, sequence):
        if not set(sequence.upper()).issubset(Sequence.Alphabet):
            raise ValueError("Entry sequence contains invalid characters")
        self._sequence = sequence

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            raise ValueError(f"Cannot compare Sequence to object of class {type(other)}")

        return self._sequence == other._sequence
