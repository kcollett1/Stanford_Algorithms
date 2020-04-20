#!/Users/kcolletti1/opt/anaconda3/bin/python3


'''
   In this code, we take as input different instances of a 2-SAT (2 satisfiability) problem.
   We implement Papadimitriou's randomized local search algorithm to solve this computationally
   intractable problem. For the smallest 2sat instance data set (2sat1.txt), this code found a
   valid assignment of variables in ~46 minutes. The other data sets are too big and thus run
   too slowly for the algorithm to compute anything in a reasonable amount of time as it is -
   so we must find a different approach.
'''


import numpy as np
import time


def main():

    if len(sys.argv) < 2:
        fname = 'scc.txt'  # default test file
    else:
        fname = sys.argv[1]

    print('\n Checking {0}'.format(fname))

    with open(fname) as data:
        n = int(next(data).strip())  # num of variables and clauses are the same in these instances
        clauses = [[0, 0] for _ in range(n)]
        for ind,line in enumerate(data):
            clauses[ind] = [int(d) for d in line.strip().split(' ')]


    def valid_clause(clause):
        var1 = variables[abs(clause[0]) - 1]
        var1 = (clause[0] < 0 and not var1) or (clause[0] > 0 and var1)
        if var1: return True

        var2 = variables[abs(clause[1]) - 1]
        return (clause[1] < 0 and not var2) or (clause[1] > 0 and var2)


    def valid_assignment():
        for clause in clauses:
            if not valid_clause(clause):
                return False
        return True

    nsq2 = 2*n*n
    log2n = int(np.log2(n))

    for i in range(log2n):  # run log_2(n) randomized experiments
        print('\n Starting randomized experiment {0} of {1}...'.format(i, log2n))

        variables = np.random.choice([True, False], size=n)

        for _ in range(nsq2):
            # check if this assignment of vars is valid or not, if it is, stop!
            if valid_assignment():
                print('This problem DOES have a valid assignment of vars! :)')
                return True

            # else, pick a random clause that's wrong, and flip one of the vars randomly
            clause = np.random.randint(n)  # pick a random clause from [0,n)
            while valid_clause(clauses[clause]):  # keep picking until we find an invalid clause
                clause = np.random.randint(n)

            var = abs(clauses[clause][np.random.randint(2)]) - 1  # pick var to change at random
            variables[var] = not variables[var]  # flip it

    print('This problem does NOT have a valid assignment of vars! :(')
    return False


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:.6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
