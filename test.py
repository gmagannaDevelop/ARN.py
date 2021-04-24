import random
from arnstruct.core.datastructures import Node, Queue, Stack, Tree
from arnstruct.parsing.parseRfam import check_token_balance
from arnstruct.core.dynamicprog import RNAStruct

node = Node("A")

queue = Queue()
stack = Stack()

for i in range(10):
    queue.enqueue(i)
    stack.push(i)


wuss_literal = "--(((-((-----)))))-(-(----)--)-"
rna_seq = "".join((random.choice("AUCG") for i in range(len(wuss_literal))))
paired = wuss_literal + "\n" + rna_seq

print(paired)

void_tree = Tree.from_parentheses(wuss_literal)
filled_tree = Tree.from_parentheses_and_sequence(wuss_literal, rna_seq)

other_wuss: str = "::::::::::::<<<<<<........________.......................................................................>>>>>>..<<<-<<<_____.......>>>->>>.<<<.______.._>>>::::"

dyn_prog_test = RNAStruct("AUGCCGCUGCAUGA")

for i in range(len(dyn_prog_test)):
    for j in range(len(dyn_prog_test)):
        print(dyn_prog_test._gamma(i, j))

# breadth_first = filled_tree.breath_first_transversal()

# rebuilt_seq_ls = []
# for i in sorted(breadth_first.keys()):
#    rebuilt_seq_ls += breadth_first[i]
#
# rebuilt_rna = "".join(elem.content for elem in rebuilt_seq_ls if elem)
