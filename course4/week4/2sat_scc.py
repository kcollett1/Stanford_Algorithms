#!/Users/kcolletti1/opt/anaconda3/bin/python3


'''
   In this code, we take as input different instances of a 2-SAT (2 satisfiability) problem.
   We implement an algorithm that constructs a graph from the variables and clauses (this is
   the "implication" graph where each variable exists on the graph as two vertices - the variable
   itself and its negation, and each clause exists as two edges where we point from the negation
   of one assertion to the truth of the other and vice versa, meaning if one of these instances is
   not true then the other has to be true: i.e. if a clause were (x1 or (not x3)) then we would
   have an edge pointing from -x1 to -x3 and another edge point from x3 to x1), and then runs the
   DFS 2-pass Kosaraju's algorithm that has been coded up from an earlier course to compute the
   strongly connected components (SCC) of the graph. If any variable and it's negation belong to
   the same SCC, we conclude the clauses can not be satisfied. Else, it indeed can be satisfied.
   If we wish to reconstruct a correct setting of the variables to satisfy the constraints, we
   simply pick one and set it, forcing other implications from there, repeatedly until all are set.
   This is a linear time algorithm! My previous attempt at solving this problem via Papadimitriou's
   local search randomized algorithm would have worked given enough time, but I don't have that
   time to wait for an answer, so I implemented this other, faster solution.
   With the largest input of 10^6 variables and 10^6 clauses, this code ran in ~41.356 seconds.
'''

from graph import Graph
import numpy as np
import sys
import time


def main():

    if len(sys.argv) < 2:
        fname = '2sat1.txt'  # default test file
    else:
        fname = sys.argv[1]

    print('\n Checking {0}'.format(fname))

    test_graph = Graph()

    with open(fname) as data:
        n = int(next(data).strip())
        # num of vars and clauses are the same in these instances, we need 2*n verts and edges
        # variable j, -j will be represented in the graph by verts 2*j-1, 2*j

        # add our vertices to the graph
        for i in range(2*n):
            test_graph.add_vert(i)

        for ind,line in enumerate(data):
            a,b = [int(d) for d in line.strip().split(' ')]
            if abs(a) == abs(b) and a*b < 0:  # trivial clause "a or not a", would be a self-loop
                continue

            # add two edges for this clause, one pointing from -a to b
            # and one pointing from -b to a
            # NOTE: a or b could be negations, so -a could actually correspond to -(-abs(a))
            var_a, var_b = 2*abs(a), 2*abs(b)
            var_nota, var_notb = 2*abs(a), 2*abs(b)
            if a > 0:
                var_a -= 1
            else:
                var_nota -= 1
            if b > 0:
                var_b -= 1
            else:
                var_notb -= 1
            test_graph.add_edge(var_nota, var_b)
            test_graph.add_edge(var_notb, var_a)

    scc_groups = test_graph.compute_scc()  # find the strongly connected components

    for _,scc in scc_groups.items():
        for var in scc:
            # for odd vert in graph, negation corresponds to vert + 1, and for even vert
            # in graph, negation corresponds to vert - 1. check if paired vert is in this SCC
            if var - 1 + 2*(var%2) in scc:
                print('\n There is NOT a setting of vars that satisfy the constraints',
                      'of this problem! :(')
                return False
            # else it is valid for this var, need to keep checking the rest

    # checked all vars in all SCC's - there DOES exist valid assignment to satisfy the prob!
    print('\n There IS a setting of vars that satisfy the constraints of this problem! :)')
    return True


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:.6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
