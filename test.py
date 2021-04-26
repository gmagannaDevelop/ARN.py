import random
import numpy as np
from arnstruct.core.datastructures import Node, Queue, Stack, Tree
from arnstruct.parsing.parseRfam import check_token_balance
from arnstruct.core.dynamicprog import RNAStruct
from arnstruct.core.parentheses import Parentheses

node = Node("A")

queue = Queue()
stack = Stack()

for i in range(10):
    queue.enqueue(i)
    stack.push(i)


wuss_literal = "--(((-((-----)))))-(-(----)--)-"
rna_seq = "".join((random.choice("AUCG") for i in range(len(wuss_literal))))
paired = wuss_literal + "\n" + rna_seq

wuss2 = "-(-(----)--)-"
seq2 = "".join((random.choice("AUCG") for i in range(len(wuss2))))
print(paired)

void_tree = Tree.from_parentheses(wuss_literal)
filled_tree = Tree.from_parentheses_and_sequence(wuss_literal, rna_seq)
filled_tree2 = Tree.from_parentheses_and_sequence(wuss_literal, rna_seq)
sub_tree = Tree.from_parentheses_and_sequence(wuss2, seq2)

other_wuss: str = "::::::::::::<<<<<<........________.......................................................................>>>>>>..<<<-<<<_____.......>>>->>>.<<<.______.._>>>::::"

dyn_prog_test = RNAStruct("CCGGCAUG")

# Test sub-trees :
print("\n\n")
print(sub_tree, "\n")
print(filled_tree, "\n")
print(f"sub_tree in tree : {sub_tree in filled_tree}")


sub_test = filled_tree.root.children[2]
sub_root = Node()
sub_root.add_child(sub_test)

sub_tree = Tree(sub_root)

print("test maximum common subtree :")
print(filled_tree.maximum_common_subtree(sub_tree))