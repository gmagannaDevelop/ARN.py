from typing import Dict
from .datastructures import Stack


class Parentheses(str):

    _token_pairs: Dict[str, str] = {"[": "]", "{": "}", "(": ")", "<": ">"}

    @staticmethod
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

        s = Stack()
        for char in expr:
            if char in Parentheses._token_pairs.keys():  # Push opening tokens
                s.push(char)
            elif char in Parentheses._token_pairs.values():  # Check for closing tokens
                try:
                    if char != Parentheses._token_pairs[s.pop()]:
                        return False
                except IndexError:
                    return False

        return True if s.is_empty() else False

    @staticmethod
    def to_parentheses(
        expr: str, replace_others: bool = True, replacing_char: str = "-"
    ) -> str:
        """
        Convert an expression with opening and closing tokens
        to an expression containing only parentheses as opening and closing
        tokens.

                    input sets          |  output sets
        opening { "<", "(", "[", "{" } -> "("
        closing { ">", ")", "]", "}" } -> ")"

        Optional parameters :
            replace_others : should non opening or closing tokens be replaced ?
            replacing_char : the char used to replace non-opening and non-closing elements in the string
        """
        _par_expr: str = ""

        for char in expr:
            # check for opening tokens :
            if char in Parentheses._token_pairs.keys():
                _par_expr += "("
            # check for closing tokens :
            elif char in Parentheses._token_pairs.values():
                _par_expr += ")"
            # default case, non-opening, non-closing token :
            else:
                _par_expr += char if not replace_others else replacing_char

        return _par_expr

    @staticmethod
    def validate_and_convert(expr: str) -> str:
        if not Parentheses.check_token_balance(expression):
            raise ValueError("Parenthesised expression is not balanced")
        else:
            return Parentheses.to_parentheses(expr)

    def __init__(self, expression: str):
        if not isinstance(expression, str):
            raise TypeError(
                f"parameter `expression` should be a String, not {type(expression)}"
            )
        if not Parentheses.check_token_balance(expression):
            raise ValueError("Parenthesised expression is not balanced")

        self._parentheses: str = Parentheses.to_parentheses(expression)
        raise NotImplementedError(
            "This class was not meant to be instantiated. Use Parentheses.validate_and_convert() instead"
        )
        # print(f"expr = {expression}, par = {self._parentheses}")
        # super().__new__(str, self._parentheses)
        # super().__new__(str, self._parentheses)

    def __repr__(self):
        return self._parentheses

    def __str__(self):
        return self._parentheses

    def __iter__(self):
        return iter(self._parentheses)

    def __contains__(self, other):
        pass