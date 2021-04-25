"""
    Core datastructures needed to represent 
    the genreal tree spawned by secondary tRNA
    structures.
"""
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
        """ Wrapper for self.size : number of elements in the queue."""
        return self.size

    def __iter__(self):
        """Iterate over the elements of the queue, in the same
        order as if queue.dequeue() was being called sequentially."""
        return iter(reversed(self.items))

    @property
    def items(self) -> List[Any]:
        """ Shallow copy of the list of elements in the queue."""
        return self._items.copy()

    @property
    def size(self) -> int:
        """ An integer representing the number of elements in the queue. """
        return len(self._items)

    def is_empty(self) -> bool:
        """boolean, returns :
        * True if the queue is empty (has zero elements)
        * False otherwise
        """
        return len(self._items) == 0

    def enqueue(self, *args) -> NoReturn:
        """ Add one (or more) elements to the queue."""
        for item in args:
            self._items.insert(0, item)

    def dequeue(self) -> Any:
        """Remove the next element in the queue if possible (the queue is not empty).
        Raises IndexError() if called on an empty queue."""
        if self.is_empty():
            raise IndexError("cannot dequeue from empty Queue")
        else:
            return self._items.pop()

    def empty(self) -> NoReturn:
        """ Empty the queue without returning the results. """
        while not self.is_empty():
            _ = self.dequeue()

    def peek(self) -> Any:
        """ Returns a view at the first element in the queue, without removing it."""
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
        """ Wrapper for self.size : number of elements in the stack."""
        return self.size

    def __iter__(self):
        """Iterate over the elements of the stack, in the same
        order as if stack.pop() was being called sequentially."""
        return iter(reversed(self.items))

    @property
    def size(self):
        """ An integer representing the number of elements in the stack. """
        return len(self._items)

    @property
    def items(self) -> List[Any]:
        """ Shallow copy of the list of elements in the stack."""
        return self._items.copy()

    def push(self, *args):
        """ Add one (or more) elements to the top of the stack. """
        for item in args:
            self._items.append(item)

    def pop(self):
        """ """
        if self.is_empty():
            raise IndexError("Cannot pop from empty Stack.")
        else:
            return self._items.pop()

    def peek(self):
        """ Returns a view at the first element in the queue, without removing it."""
        return self._items[-1]

    def is_empty(self):
        """boolean, returns :
        * True if the stack is empty (has zero elements)
        * False otherwise
        """
        return len(self._items) == 0


class Node(object):
    """
    Node base class used to represent a general (rooted) tree.

    A general tree is defined as a tree having nodes with an arbitrary'
    number of children each.

    Here we use a linked list implementation, where each node has a reference
    to its first child, which contains a list of references to its siblings
    (nodes found in the tree, at the same depth).

    Example :

                    root
                /     |    \\
                A     B     C
                     / \\  
                    D    E

    is represented as :

    root
    |
    first_child(A) -> [second_child(B), third_child(C)]
                         |
                       first_child(D) -> [second_child(E)]

    Note :  magic methods are implemented for the implementation of the ARN
    general tree but are not meant to be used by final users.

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

    def __eq__(self, other: "Node"):
        if not isinstance(other, Node):
            raise TypeError(
                f"Cannot compare instance of Node to instance of {type(other)}"
            )
        else:
            return self.content == other.content

    # TODO : remove as it is not used ?
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
        """ A unique representation of the node, given by its memory address."""
        return self.__uuid

    @property
    def content(self) -> Any:
        """ The content of the node."""
        return self._content

    @property
    def siblings(self) -> List["Node"]:
        """ Return a shallow copy of the siblings of the node"""
        return self._siblings.copy()

    @property
    def first_child(self):
        """First child of node, according to the chained
        representation described in the main docstring."""
        return self._first_child

    @property
    def children(self):
        """Return a list of the first child and all of its siblings,
        which together represent all the children of the node."""
        if self.first_child is not None:
            return [self.first_child] + self.first_child.siblings
        else:
            return None

    def add_child(self, child: "Node") -> NoReturn:
        """Add a child to a node. Given the chained implementation this
        means modifying the `self._first_child` property for leaf nodes.
        If the node is not a leaf, the node (param `child`) will be added
        to the siblings of the first_child of the current node.

        Raises TypeError if `child` is not an instance of Node.
        """
        if not isinstance(child, Node):
            raise TypeError(self.__type_error(child))

        if not self._first_child:
            self._first_child = child
        else:
            self._first_child.add_sibling(child)

    def add_sibling(self, node: "Node") -> NoReturn:
        """Add a sibling to the current node.

        Raises TypeError if `node` is not an instance of Node.
        """
        if not isinstance(node, Node):
            raise TypeError(self.__type_error(node))
        else:
            self._siblings.append(node)

    def add_siblings(self, *args) -> NoReturn:
        """Add a sibling to the current node for each arg in args.

        Raises TypeError if any of `args` is not an instance of Node.
        """
        _are_nodes: List[bool] = [isinstance(arg, Node) for arg in args]
        # check that all siblings are nodes :
        if not all(_are_nodes):
            raise TypeError(f"One (or more) argument(s) are not instance(s) of Node.")
        else:
            for arg in args:
                self.add_sibling(arg)

    def is_leaf(self):
        """ Return True if the node has no children, False otherwise."""
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
    """
    General tree built from a WUSS-format parenthesised expression.

    It represents the secondary structure of tRNA molecules.
    """

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

    def __repr__(self) -> str:
        elems: List[str] = [
            "RNA Secondary Structure tree",
            f" Structure : {self.to_parentheses()}",
            f" Sequence  : {self.to_sequence()}",
        ]
        return "\n".join(elems)

    def is_empty(self):
        """Return True if there are no nodes other than the root
        i.e. the root is a leaf (has no children)."""
        return self._root.is_leaf()

    @property
    def root(self):
        """ Return a reference to the root of the tree. """
        return self._root

    # TODO : find a utility for this or remove it
    def _breath_first_transversal(self):
        """ DO NOT CALL, experimental. """
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
        """Private method to be called before and after a call to
        self._depth_first_transversal()."""
        self.__elements = []

    def to_sequence(self) -> str:
        """Rebuild the character sequence that generated the tree contentents.
        The string is built by performing a `depth first transversal`
        on a copy of the tree."""
        self.__reset_elements()
        self._depth_first_transversal(mode="sequence")
        sequence: str = "".join(self.__elements)
        self.__reset_elements()
        return sequence

    def to_parentheses(self) -> str:
        """Rebuild the parenthesised expression that generated the tree structure.
        The string is built by performing a `depth first transversal`
        on a copy of the tree."""
        self.__reset_elements()
        self._depth_first_transversal(mode="parenthesis")
        parentheses: str = "".join(self.__elements)
        self.__reset_elements()
        return parentheses

    def to_wuss_format(self) -> str:
        """ Wrapper for self.to_parentheses() """
        return self.to_parentheses()

    def _depth_first_transversal(
        self,
        mode: str,
        node: Optional[Node] = None,
        pairs_stack: Optional[Stack] = None,
    ) -> NoReturn:
        """Perform a depth-first transversal on a copy of the Tree.
        This method needs to operate on a copy and not the tree itself because
        modifies the content of nodes which represent base pairs in the structure.

        This method will modify a private instance attribute self.__elements
        which is used to rebuild the sequence and/or parenthesised expression
        that the tree represents.
        """
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
