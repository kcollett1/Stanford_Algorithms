#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
    We are given a list of input numbers (there are about a million numbers,
    ranging from roughly -10^11 to 10^11). Our goal is to find the number of
    pairs within this data set that sum up to a target value within the range
    [-10^4, 10^4] (inclusive). With some inspection of the data, we can see that
    the numbers in this data set are pretty uniformally distributed over the
    range of possible values, which allows us to cut our search space down
    dramatically if we do some pre-processing of the numbers first.
    if we split a number into "buckets" of 10^4 and  map that to their mod10^4,
    i.e. 24,600 would be in bucket 2 since 24,600//10,000 = 2, and would be
    mapped to 4,600 since 24,600%10,000 = 4,600 (Note, this also works for
    negatives). We can use the bucket number to be our key in our dict, and for
    each bucket/key, we will store the set of remainders (ignoring duplicates)
    of all numbers in the data. This is where the uniform distribution of our
    data is useful - if most numbers were clumped around one value/bucket, that
    bucket would still hold most of the numbers and other buckets would be mostly
    empty, and our search space/number of comparisons we need to make has not
    been reduced by much, but with the data we have, each bucket winds up only
    holding between 1 and 5 numbers, which is a dramatic reduction from 10^6!
    Through this splitting of the number, we only have to check buckets that may
    contain numbers that could add up to a number between -10^4 and 10^4. For
    example if we took the number 4,600,214, obviously any positive number will
    not work, and actually only a small range (20,000) of negative numbers will
    satisfy this criteria, so if we see this number, we know we only have to look
    through a couple of negative buckets. It can be shown in general, that if a
    number is in bucket x, we only have to look through buckets -x-2, -x-1, -x, -x+1
    Any number outside of those buckets will not give us a sum within our range.
    This code took about ~4 seconds to execute.
'''


import numpy as np
import time


def main():
    data = {}  # hash structure, {bucket#: mod value}
    up_range = 10000
    t_found = np.array([False for _ in range(2*up_range + 1)])
    # index in t_found = [0,2*up_range]; so t = ind - up_range; when recording t, rmbr to shift!

    with open('two_sum.txt') as datafile:
        for num in datafile:
            num = int(num.strip())
            bucket = num // up_range
            remain = num % up_range  # also works just fine for negative values!

            # for bucket x, need to possibly check buckets (-x-2, -x-1, -x, -x+1)
            # each bucket in this algo is basically O(1) size, so this is still 4*O(1)
            for check_bucket in (-bucket + i for i in range(-2, 2)):
                if check_bucket in data:  # O(1) hash look up time
                    base_num = up_range * check_bucket
                    for mod_num in data[check_bucket]:
                        check_num = base_num + mod_num
                        target = num + check_num
                        if target >= -up_range and target <= up_range:  # found a pair
                            t_found[target + 10000] = True

            # finally add this number to our data hash dictionary, for future comparisons
            if bucket in data:  # O(1) hash look up time
                data[bucket].add(remain)  # bc of hash structure, we won't track duplicate nums
            else:
                data[bucket] = {remain}  # using hash structure within dict hash structure!

    print('\n The number of target values in range [-10000, 10000]\n with distinct',
          'values in arr that sum to it are', np.sum(t_found))

    print('\n The target values found were:\n',
          np.array(np.where(t_found)) - up_range, '\n')

    #########################################################################
    ## just analyzing how distributed the data became after putting         #
    ## it into these buckets each bucket can contain UP TO up_range         #
    ## different numbers, which could be very large if we indeed have that  #
    ## distribution from our input data, but that would still be the best   #
    ## this particular algo could do to find the number of target values    #
    #                                                                       #
    #bucket_sizes = set()                                                   #
    #for bucket in data: bucket_sizes.add(len(data[bucket]))                #
    #print('there are', len(data), 'buckets total to go through,',          #
    #      'but each bucket only has anywhere from', min(bucket_sizes),     #
    #      'to', max(bucket_sizes), 'numbers within it! :)')                #
    #########################################################################


if __name__ == "__main__":

    t0 = time.time()
    main()
    t1 = time.time()

    print('With pythons built-in hash structures,',
           'code took {0:.2f} seconds to run.'.format(t1-t0))

    raise SystemExit
