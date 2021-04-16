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

__all__ = ["Queue", "Node", "Tree"]


class Queue(object):
    """
    Basic Queue implemented on a list.

    The complexity of Queue operations is :

    * enqueue O(n)
    * dequeue O(1)
    * peek    O(1)
    """

    def __init__(self):
        self._items: List[Any] = []

    def __repr__(self):
        return f"Queue ({self._items})"

    def __len__(self):
        return self.size

    @property
    def items(self) -> List[Any]:
        """ Shallow copy of the list of elements in the Queue."""
        return self._items.copy()

    @property
    def size(self) -> int:
        """ """
        return len(self._items)

    def is_empty(self) -> bool:
        """ """
        return len(self._items) == 0

    def enqueue(self, *args) -> NoReturn:
        """ """
        for item in args:
            self._items.insert(0, item)

    def dequeue(self) -> Any:
        """ """
        return self._items.pop()

    def peek(self) -> Any:
        """ """
        return self.items[-1]


class Node(object):
    """ """

    def __init__(self, content: Optional[Any] = None):
        self.__uuid = hex(id(self))
        self._content: Any = content
        self._first_child: Union[Node, None] = None
        self._siblings: List[Node] = []

    def __repr__(self):
        return f"Node({self.content})"

    def __str__(self):
        return f"{self.content}"

    @property
    def id(self):
        return self.__uuid

    @property
    def content(self) -> Any:
        """  """
        return self._content

    @property
    def siblings(self) -> List["Node"]:
        """ """
        return self._siblings.copy()

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
    """ """

    pass