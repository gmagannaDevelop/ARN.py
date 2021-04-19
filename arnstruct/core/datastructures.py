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

import copy

__all__ = ["Queue", "Stack", "Node", "Tree"]


class Queue(object):
    """
    Basic Queue implemented on a Python list.

    The complexity of Queue operations is :

    * enqueue O(n)
    * dequeue O(1)
    * peek    O(1)
    * empty   O(n)
    """

    def __init__(self):
        self._items: List[Any] = []

    def __repr__(self):
        return f"Queue : {self._items}-> head"

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter(reversed(self.items))

    @property
    def items(self) -> List[Any]:
        """ Shallow copy of the list of elements in the Queue."""
        return self._items.copy()

    @property
    def size(self) -> int:
        """ An integer representing the number of elements in the Queue. """
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
        if self.is_empty():
            raise IndexError("cannot dequeue from empty Queue")
        else:
            return self._items.pop()

    def empty(self) -> NoReturn:
        """ """
        while not self.is_empty():
            _ = self.dequeue()

    def peek(self) -> Any:
        """ """
        return self.items[-1]


class Stack(object):
    """
    Basic implementation of a Stack on a Python list().

    The complexity of Stack operations is :

    * push  O(1)
    * pop   O(1)
    * peek  O(1)
    * empty O(n)
    """

    def __init__(self):
        self._items = []

    def __repr__(self):
        return f"Stack : {self._items} -> head"

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter(reversed(self.items))

    @property
    def size(self):
        """ """
        return len(self._items)

    @property
    def items(self) -> List[Any]:
        """ Shallow copy of the list of elements in the Stack."""
        return self._items.copy()

    def push(self, *args):
        """ """
        for item in args:
            self._items.append(item)

    def pop(self):
        """ """
        if self.is_empty():
            raise IndexError("Cannot pop from empty Stack.")
        else:
            return self._items.pop()

    def peek(self):
        """ """
        return self._items[-1]

    def is_empty(self):
        """ """
        return len(self._items) == 0


class Node(object):
    """
    Note : len(Node) is particularly defined for nodes having a Queue
    as content.
    """

    @staticmethod
    def __type_error(x: Any) -> str:
        """ """
        return "\n".join(
            [
                f"Cannot add object `x` of type {type(x)} to a Tree.",
                f"Try adding `Node(x)` instead.",
            ]
        )

    def __init__(self, content: Optional[Any] = None):
        self.__uuid = hex(id(self))
        self._content: Any = content
        self._first_child: Union[Node, None] = None
        self._siblings: List[Node] = []

    def __repr__(self):
        return f"Node({self.content})"

    def __bool__(self):
        return True

    def __str__(self):
        return f"{self.content}"

    def __len__(self):
        _iter_types = [Queue, Stack, list]
        # check if we can get the length of contents :
        _is_iterable = any(isinstance(self._content, i) for i in _iter_types)
        if self._content is None:
            # if there is no content
            return 0
        elif _is_iterable:
            # if content is an iterable collection
            return len(self._content)
        else:
            # if content is a single element
            return 1

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

    def add_child(self, child: "Node") -> NoReturn:
        """ """
        if not isinstance(child, Node):
            raise TypeError(self.__type_error(child))

        if not self._first_child:
            self._first_child = child
        else:
            self._first_child.add_sibling(child)

    def add_sibling(self, node: "Node") -> NoReturn:
        """ """
        if not isinstance(node, Node):
            raise TypeError(self.__type_error(node))
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

    def is_leaf(self):
        """ """
        return True if self.children is None else False

    def content_is_iterable(self) -> bool:
        """ Check if the content of a node is iterable by duck-typing """
        try:
            _ = iter(self._content)
            return True
        except TypeError:
            return False

    def content_isinstance(self, cls) -> bool:
        """ wrapper for isinstance(self._content, cls) """
        return isinstance(self._content, cls)


class Tree(object):
    """ """

    @classmethod
    def from_parentheses(cls, parentheses: str):
        """ """
        stack: Stack = Stack()
        root: Node = Node()

        stack.push(root)

        for char in parentheses:
            if char == "(":
                new_node = Node()
                parent = stack.pop()
                parent.add_child(new_node)
                stack.push(parent)
                stack.push(new_node)
            elif char == "-":
                new_node = Node()
                parent = stack.pop()
                parent.add_child(new_node)
                stack.push(parent)
            else:
                stack.pop()

        return cls(stack.peek())

    @classmethod
    def from_parentheses_and_sequence(cls, parentheses: str, sequence: str):
        """ """
        stack: Stack = Stack()
        root: Node = Node()
        # stack to keep trace of opening and closing braces
        balance_stack: Stack = Stack()

        stack.push(root)

        # TODO : verify edge cases :
        for char, base in zip(parentheses, sequence):
            if char == "(":
                new_node = Node(Queue())
                new_node.content.enqueue(base)
                # to be able to add the corresponding matching base
                balance_stack.push(new_node)
                parent = stack.pop()
                parent.add_child(new_node)
                stack.push(parent)
                stack.push(new_node)
            elif char == "-":
                new_node = Node(base)
                parent = stack.pop()
                parent.add_child(new_node)
                stack.push(parent)
            elif char == ")":
                balance_stack.peek().content.enqueue(base)
                balance_stack.pop()
                stack.pop()
            else:
                raise ValueError(
                    f"Parenthesised expression contains unknown character {char}"
                )

        return cls(stack.peek())

    def __init__(self, root: Node):
        self._root = root
        self.__elements: List[str] = []

    def is_empty(self):
        """Return True if there are no nodes other than the root
        i.e. the root is a leaf (has no children)."""
        return self._root.is_leaf()

    @property
    def root(self):
        return self._root

    def breath_first_transversal(self):
        """ """
        queue: Queue = Queue()
        queue.enqueue(self._root)
        level_queue: Queue = Queue()

        tree_map: Dict[int, Node] = {0: [self._root]}
        level: int = 0

        while not queue.is_empty():
            current: Queue = queue.dequeue()
            print(current.content, end="")
            if current.children is not None:
                level += 1
                for child in current.children:
                    queue.enqueue(child)
                    level_queue.enqueue(child)

                tree_map.update({level: level_queue.items})
                level_queue.empty()

    def __reset_elements(self):
        """ """
        self.__elements = []

    def to_sequence(self) -> str:
        """ """
        self.__reset_elements()
        self._depth_first_transversal(mode="sequence")
        sequence: str = "".join(self.__elements)
        self.__reset_elements()
        return sequence

    def to_parentheses(self) -> str:
        """ """
        self.__reset_elements()
        self._depth_first_transversal(mode="parenthesis")
        parentheses: str = "".join(self.__elements)
        self.__reset_elements()
        return parentheses

    def to_wuss_format(self) -> str:
        """ """
        return self.to_parentheses()

    def _depth_first_transversal(
        self,
        mode: str,
        node: Optional[Node] = None,
        pairs_stack: Optional[Stack] = None,
    ) -> NoReturn:
        """ """
        _valid_modes: List[str] = ["sequence", "parenthesis"]
        if mode not in _valid_modes:
            raise ValueError(f"Unknown mode {mode}. Valid modes are : {_valid_modes}")

        node: Node = node or self.root
        node = copy.deepcopy(node)
        pairs_stack: Stack = pairs_stack or Stack()

        if node.content_isinstance(str):
            if mode == _valid_modes[0]:
                self.__elements.append(node.content)
            else:
                self.__elements.append("-")

        elif node.content_isinstance(Queue):
            if mode == _valid_modes[0]:
                self.__elements.append(node.content.dequeue())
                pairs_stack.push(node.content.dequeue())
            else:
                self.__elements.append("(")
                pairs_stack.push(None)

        if not node.is_leaf():
            for child in node.children:
                self._depth_first_transversal(mode, child, pairs_stack)

            if not pairs_stack.is_empty():
                if mode == _valid_modes[0]:
                    self.__elements.append(pairs_stack.pop())
                else:
                    self.__elements.append(")")
                    pairs_stack.pop()
