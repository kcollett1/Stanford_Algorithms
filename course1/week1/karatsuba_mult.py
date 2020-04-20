
# this is my implementation of karatsuba's algorithm

def karatsuba_mult(x: int, y: int)-> int:
    ''' this function multiplies two integers using karatsubas algorithm
    '''
    # allow for multiplication of negative numbers as well
    neg = 1
    if x < 0:
        neg = -1
        x = abs(x)
    if y < 0:
        neg *= -1
        y = abs(y)

    # base cases: either of the numbers is 0 or both are single digit
    if x == 0 or y == 0:
        return 0
    elif x < 10 and y < 10:
        return x * y

    x,y = str(x),str(y)
    n = max(len(x), len(y))
    if len(y) < n:
        y = y.zfill(n)
    elif len(x) < n:
        x = x.zfill(n)
    half = n // 2 + n % 2

    a,b = int(x[:half]),int(x[half:])
    c,d = int(y[:half]),int(y[half:])

    ac = karatsuba_mult(a, c)
    bd = karatsuba_mult(b, d)
    adbc = karatsuba_mult(a+b, c+d) - ac - bd

    # add n (or n - 1) 0's to ac
    ac = int(str(ac) + '0'*(n - n%2))
    # add n//2 0's to adbc
    adbc = int(str(adbc) + '0'*(n//2))

    return neg * (ac + adbc + bd)

x = 3141592653589793238462643383279502884197169399375105820974944592
y = 2718281828459045235360287471352662497757247093699959574966967627
#x = 2925
#y = 6872
print('multiplying', x, 'and', y, 'with the karatsuba algorithm')
prod = karatsuba_mult(x, y)
print('answer is:', prod)
