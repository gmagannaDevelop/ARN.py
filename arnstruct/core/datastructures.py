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
        return bool(self.content)

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
                # new_node = Node(base)
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

    @property
    def root(self):
        return self._root

    def breath_first_transversal(self):
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
