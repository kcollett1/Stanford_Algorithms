# this is a recursive algorithm to multiply two integers together

def recursive_mult_verynaive(x: int, y: int)-> int:
    ''' this function recursively multiplies two integers x and y
        based on the relation x*y = (x-1)*(y-1) + x + y - 1
        when expanding (x-1)*(y-1) we get x*y - x - y + 1
        which is where the extra additive factors come from in our recursive step
        as we need to subtract out the extra terms to arrive at the correct answer
    '''
    # base case, x or y is 0, return 0
    if x == 0 or y == 0:
        prod = 0
    # base case, x or y is 1, return y or x, respectively
    elif x == 1:
        prod = y
    elif y == 1:
        prod = x
    else:
        prod = recursive_mult(x-1, y-1) + x + y - 1

    return prod

def recursive_mult_naive(x: int, y: int)-> int:
    ''' this function uses recursion to mutliply two numbers
        using relation x*y = 10**n*a*c + 10**n/2*(a*d + b*c) + b*d
        where x=ab and y=cd (the numbers are split in half as if strings
        i.e. if x=1234 then a=12, b=34). recursively compute the four products
        and then combine them together to get final result, padding numbers
        with appropriate number of 0's
    '''
    # base case, x or y is 0, return 0
    if x == 0 or y == 0:
        return 0
    # allow for negative number multiplication
    neg = 1
    if x < 0:
        x = abs(x)
        neg = -1
    if y < 0:
        y = abs(y)
        neg *= -1

    # base case, x and y are single digits
    if x < 10 and y < 10:
        return neg*x*y

    x,y = str(x), str(y)
    if len(x) < len(y):
        x = x.zfill(len(y))
    if len(y) < len(x):
        y = y.zfill(len(x))
    n = len(x)
    half = n//2 + n%2
    a,b = x[:half], x[half:]  # if odd, a and c have extra element
    c,d = y[:half], y[half:]

    ac = int(str(recursive_mult_naive(int(a), int(c))) + '0'*(n - n%2))
    adbc = int(str(recursive_mult_naive(int(a), int(d)) + recursive_mult_naive(int(b), int(c))) + '0'*(n//2))
    bd = recursive_mult_naive(int(b), int(d))

    return neg*(ac + adbc + bd)

x = 3141592653589793238462643383279502884197169399375105820974944592
y = 2718281828459045235360287471352662497757247093699959574966967627
#x = 123
#y = 123
print('multiplying', x, 'and', y, 'recursively...')
print('answer is:', recursive_mult_naive(x, y))
# ERROR: maximum recursion depth exceeded in comparison, does not work for large numbers for verynaive algo
