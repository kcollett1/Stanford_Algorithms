# this is my implementation of the method we were taught to multiply numbers in grade school

def gradeschool_mult(x: int, y: int)-> int:
    ''' multiply two integers using the grade-school method
    '''
    # allow for negative integer multiplication
    neg = 1
    if x < 0:
        neg = -1
        x = abs(x)
    if y < 0:
        neg *= -1
        y = abs(y)

    # format to loop over digits and initialize answer list to store digits as we multiply
    x = str(x)
    y = str(y)
    prod = [0 for _ in range(len(x) + len(y))]

    # for each digit in x, multiply it by all the digits in y, in reverse order taking carries into account
    for strt,n in enumerate(x[::-1]):
        carry = 0
        for ind,m in enumerate(y[::-1], start=strt):
            nm = str(int(n) * int(m) + carry).zfill(2)
            prod[ind] += int(nm[-1])
            carry = int(nm[:-1])
        if carry:
            prod[strt + len(y)] += carry

    # some of the summing up step has been done in the previous step, but we need to now take final carry values into account
    carry = 0
    for i,s in enumerate(prod):
        s = str(s + carry).zfill(2)
        prod[i] = int(s[-1])
        carry = int(s[:-1])
    if carry:
        prod.append(carry)

    # ans is in reverse order in prod list, format it correctly and make it negative if needed to return final result
    return neg * int(''.join([str(i) for i in prod[::-1]]))

x = 3141592653589793238462643383279502884197169399375105820974944592
y = 2718281828459045235360287471352662497757247093699959574966967627
print(x,'times',y,'=\n',gradeschool_mult(x, y))
