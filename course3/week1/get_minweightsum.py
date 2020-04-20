#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
    The goal of this algorithm is to calculate the minimum weighted sum of completion times of
    given input jobs. The weighted completion time is defined to be the time when the job
    finishes running multiplied by the jobs weight. We are given as input 10,000 jobs (their
    length and weight). We use here two greedy algorithms to compute the answer, though we know
    one is wrong. To rank the jobs to decide what order to schedule them in, we use two different
    simple metrics: the difference between the jobs weight and length, and the ratio between the
    jobs weight and length. The ratio metric (with ties broken arbitrarily), can be proven to be
    a correct algorithm, while it's easy to show by contradiction the incorrectness of the
    difference metric. Calculating the metrics for every job is O(n), and then I use my quicksort
    algo implemented in a previous course to sort both by difference and ratio (with the algo
    slightly modified to keep track of the index the element came from in the original list).
    After sorted, we can then go through in O(n) time again all of the jobs, adding their weighted
    completion time to the total. For the difference metric, we break ties by weight (i.e. for two
    jobs that have the same difference score, we schedule the job with the higher weight first).
    For the ratio metric, we break ties arbitrarily (and always arrive at the correct answer). Just
    for fun, I also test out some randomized orderings of job schedules to compare their weighted
    completion time sums to the minimum we compute. This code took about ~0.18631 seconds to execute.
'''


from quick_sort import *
from numpy import random as rand
import time


def main():
    rand.seed(42)

    with open('jobs.txt') as datafile:
        num_jobs = int(next(datafile).strip())
        jobs = [0 for _ in range(num_jobs)]  # will contain tuple of (weight_i, length_i)
        S_diff = [0 for _ in range(num_jobs)]
        S_ratio = [0 for _ in range(num_jobs)]
        weight_sum_diff = 0
        weight_sum_ratio = 0
        # just for fun, calculate weighted completion times for several randomized schedules
        rand_scheds = 10
        weight_sum_rand = [0 for _ in range(rand_scheds)]

        for itr,line in enumerate(datafile):  # O(n), const work within this loop
            jobs[itr] = tuple(int(i) for i in line.strip().split(' '))
            S_diff[itr] = jobs[itr][0] - jobs[itr][1]
            S_ratio[itr] = jobs[itr][0] / jobs[itr][1]

        # sort (in non-decreasing order) by S_diff values, and S_ratio values - O(nlog(n))
        # but also maintain the indices of the sorted order corresponding to the job number
        S_diff = quick_sort(S_diff, 0, num_jobs)
        S_ratio = quick_sort(S_ratio, 0, num_jobs)

        # before we proceed, we need to break ties in the S_diff values by decreasing job weight
        S_diff = S_diff[::-1]
        end = 0
        while end < num_jobs:
            start = end

            # increment end itr while we have ties by the difference metric
            while end < num_jobs and S_diff[end][0] == S_diff[start][0]:
                end += 1

            if end < start + 2:  # no ties for this S_diff val
                continue

            # else, need to sort S_diff[start:end] (not including end) by job weight
            diff = S_diff[start][0]
            weights = sorted([[jobs[i[1]][0], i[1]] for i in S_diff[start:end]])[::-1]
            for ind,weight in enumerate(weights, start=start):
                S_diff[ind] = [diff, weight[1]]


        # calculate the weighted sum of completion times from the given orders now - O(n)
        time_sum = 0
        for ind in S_diff:
            ind = ind[1]
            time_sum += jobs[ind][1]
            weight_sum_diff += (jobs[ind][0] * time_sum)


        time_sum = 0
        for ind in reversed(S_ratio):  # we can break ties arbitrarily when we use the ratio metric
            ind = ind[1]
            time_sum += jobs[ind][1]
            weight_sum_ratio += (jobs[ind][0] * time_sum)


        for itr in range(rand_scheds):  # calculate 10 random schedules
            time_sum = 0
            weight_sum = 0
            for ind in rand.permutation(num_jobs):
                time_sum += jobs[ind][1]
                weight_sum += (jobs[ind][0] * time_sum)
            weight_sum_rand[itr] = weight_sum


    print('\n The sum of weighted completion times calculated from using the diff between\n',
          ' weight and length of a job as the score metric is: {0}'.format(weight_sum_diff))

    print('\n The sum of weighted completion times calculated from using the ratio between\n',
          ' weight and length of a job as the score metric is: {0}'.format(weight_sum_ratio))

    print('\n And the sums of weighted completion times calculated from generating random',
          'schedules are:\n ', ', '.join(['{0:e}'.format(wsr) for wsr in weight_sum_rand]))


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\nThis code took {0:.5f} seconds to run.'.format(t1-t0), '\n')

    raise SystemExit
