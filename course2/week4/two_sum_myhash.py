#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   Performance comparison:
    This code is meant simply to test the performance of my own implementation of
    a hash dictionary, in comparison to using the built-in python dict/set.
    Using python's dict and set, code executed in ~4 seconds.
    Using my hash dict but still pythons set for the val associated with each key,
    code executed in ~20 seconds.
'''


from hashdict import HashDict
import numpy as np
import time


def main():
    data = HashDict()  # my quick and dirty hash structure, {key=bucket#: val=set of remainders/mods}
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
                if data.search(check_bucket):  # O(1) hash look up time
                    base_num = up_range * check_bucket
                    for mod_num in data.get(check_bucket):
                        check_num = base_num + mod_num
                        target = num + check_num
                        if target >= -up_range and target <= up_range:  # found a pair
                            t_found[target + 10000] = True

            # finally add this number to our data hash dictionary, for future comparisons
            if data.search(bucket):  # O(1) hash look up time
                data.get(bucket).add(remain)  # bc of hash structure, we won't track duplicate nums
            else:
                data.insert(bucket, {remain})  # using pythons set hash structure within dict hash structure!

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

    print('With my quick and dirty implementation of a hash structure,',
           'code took {0:.2f} seconds to run.'.format(t1-t0))

    raise SystemExit
