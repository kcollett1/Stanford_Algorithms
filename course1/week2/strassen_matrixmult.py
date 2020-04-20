''' my implementation of strassen's (1969) divide-and-conquer matrix multiplication
    algorithm that improved over the naive divide-and-conquer approach which was still
    O(n^3). using a master method analysis of this algorithm, it can be shown that it
    is ~O(n^2.8), as it uses 7 recursive calls rather than 8, which improves running time.
'''

import numpy as np


def strassen_recursive(x: np.ndarray, y: np.ndarray, n: int) -> np.ndarray:
    '''
        this function handles the recursion of strassens matrix multiplication
        algorithm, after the main call has handled array pre-processing.
    '''
    # base case, n = 1 (n is guaranteed to be a power of 2 so we should never see n=0 in this function)
    if n == 1:
        return x * y

    half = n // 2
    a,b,c,d = (x[:half,:half], x[:half,half:], x[half:,:half], x[half:,half:])
    e,f,g,h = (y[:half,:half], y[:half,half:], y[half:,:half], y[half:,half:])

    # recursively compute the 7 matrix products
    p1 = strassen_recursive(a, f - h, half)
    p2 = strassen_recursive(a + b, h, half)
    p3 = strassen_recursive(c + d, e, half)
    p4 = strassen_recursive(d, g - e, half)
    p5 = strassen_recursive(a + d, e + h, half)
    p6 = strassen_recursive(b - d, g + h, half)
    p7 = strassen_recursive(a - c, e + f, half)

    # put them together to make the 4 quadrants in resulting matrix product
    q1 = p4 + p5 + p6 - p2
    q2 = p1 + p2
    q3 = p3 + p4
    q4 = p5 + p1 - p3 - p7

    # put quadrants together to make final result
    return np.vstack(( np.hstack((q1, q2)), np.hstack((q3, q4)) ))


def strassen_matrixmult(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    '''
        multiply any two square matrices (of the same dimensions) using strassens
        divide-and-conquer algorithm.
    '''
    l = len(x)

    assert l == len(x[0]) and len(y) == len(y[0]) and l == len(y), 'Matrices should be square and of the same size.'

    # check we don't have empty matrices or size 1 by 1
    if l < 2:
        return x * y

    n = int(2 ** np.ceil(np.log2(l)))
    add = n - l
    x = np.array(x)
    y = np.array(y)

    # pad with zeros to make the matrices n by n where is the closest higher power of two
    # pre-process here and then invoke recursive strassen algorithm, for efficiency purposes
    if add > 0:
        x = np.hstack(( np.vstack((x, np.zeros((add, l)))), np.zeros((n, add))))
        y = np.hstack(( np.vstack((y, np.zeros((add, l)))), np.zeros((n, add))))

    return strassen_recursive(x, y, n)[:l,:l]

if __name__ == "__main__":
    test_mat_a = np.array([[i+1 for i in range(6)] for _ in range(6)])
    test_mat_b = np.array([[i+1 for i in range(6)] for _ in range(6)])

    print('multiplying two matrices:\n', test_mat_a, '\nand\n', test_mat_b)

    prod_mat_c = strassen_matrixmult(test_mat_a, test_mat_b)

    print('\n\nresult is:\n', prod_mat_c)

    raise SystemExit
