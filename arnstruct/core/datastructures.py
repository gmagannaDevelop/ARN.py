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
    Iterable,
)


class Node(object):
    """ """

    def __init__(self, content: Optional[Any] = None):
        self._content: Any = content
        self._first_child: Union[Node, None] = None
        self._siblings: List[Node] = []

    def __repr__(self):
        return f"Node({self.content})"

    def __str__(self):
        return f"{self.content}"

    @property
    def content(self) -> Any:
        """  """
        return self._content

    @property
    def siblings(self) -> List["Node"]:
        """ """
        return self._siblings

    @property
    def first_child(self):
        """ """
        return self._first_child

    @property
    def children(self):
        """ """
        if self.first_child is not None:
            return [self.first_child] + self.first_child.siblings
        else:
            return None

    def add_sibling(self, node: "Node") -> NoReturn:
        """ """
        if not isinstance(node, Node):
            err_lines: List[str] = [
                f"Cannot add object `x` of type {type(node)} to a Tree.",
                f"Try calling `add_sibling(Node(x))`",
            ]
            raise TypeError("\n".join(err_lines))
        else:
            self._siblings.append(node)

    def add_siblings(self, *args) -> NoReturn:
        """ """
        _are_nodes: List[bool] = [isinstance(arg, Node) for arg in args]
        # check that all siblings are nodes :
        if not all(_are_nodes):
            raise TypeError(f"One (or more) argument(s) are not instances of Node.")
        else:
            for arg in args:
                self.add_sibling(arg)


class Tree(object):
    """"""
