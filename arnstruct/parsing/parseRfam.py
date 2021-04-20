import pathlib
from typing import Dict, Optional, Union, NoReturn, List, Tuple, Type, Any

from ..core.datastructures import Stack


def check_token_balance(expr: str) -> bool:
    """
    Check if an expression with opening and closing tokens is balanced
    i.e. for each opening token { "<", "(", "[", "{" } its corresponding
    closing token { ">", ")", "]", "}" } is present in the string.

    The balance check is performed using a Stack which means that
    arbitrarily nested expressions are allowed.

    This function uses an early rejection strategy which means that whenever
    a closing token is found, if the closing token at the top of the stack is
    not its complement, the function will not bother checking the rest of the
    string and will simply return False.
    """

    token_pairs: Dict[str, str] = {"[": "]", "{": "}", "(": ")", "<": ">"}

    s = Stack()
    for char in expr:
        if char in token_pairs.keys():  # Push opening tokens
            s.push(char)
        elif char in token_pairs.values():  # Check for closing tokens
            try:
                if char != token_pairs[s.pop()]:
                    return False
            except IndexError:
                return False

    return True if s.is_empty() else False


class StockholmParser(object):
    """ """

    __valid_file_classes: List[Type] = [str, pathlib.Path]

    __special_tokens: Dict[str, str] = {
        "begin": "# STOCKHOLM",
        "end": "//",
    }

    @staticmethod
    def __type_error(x: Any) -> str:
        """ """
        return "\n".join(
            [
                f"Cannot read from object of class {type(x)}",
                "Please provide a string or pathlib.Path instance",
                "pointing to a readable file on disk.",
            ]
        )

    def __init__(self):
        pass

    def __call__(self, filename: Union[str, pathlib.Path]):
        """ """
        _is_valid_instance: bool = any(
            isinstance(filename, allowed) for allowed in self.__valid_file_classes
        )
        if not _is_valid_instance:
            raise TypeError(self.__type_error(filename))

        with open(filename, "r") as f:
            lines: List[str] = [line.strip() for line in f.readlines()]
