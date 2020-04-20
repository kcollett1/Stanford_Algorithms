#!/Users/kcolletti1/opt/anaconda3/bin/python3

'''
   We take as input data consisting of two strings (don't have to be of the same
   length) with characters from some input defined alphabet (i.e. for genomic
   sequencing it is [A,C,G,T]). We simply assume in this algorithm that a penalty
   for matching a character with a gap is 1 and matching a character with a different
   character is also 1, while matching a character with the same character is 0. We
   use a dynamic programming approach to finding the optimal solution which minimizes
   the penalty score of the alignment, using recursion instead of iteration to avoid
   computing any unnecessary sub-solutions that we may not need to.
   This code ran in ~0.000253 seconds.
'''


import time


def main():
    S1 = 'AGGGCT'
    S2 = 'AGGCA'
    sub_solns = {}  # hash structure to store already calculated sub-solutions

    def find_opt_score(s1, s2):
        key = 'w1{0}w2{1}'.format(s1, s2)

        if key in sub_solns:  # if we've seen this problem already, just return result
            return sub_solns[key]

        # base cases to stop recursion - either string is empty (the rest of the
        # longer word (if not both empty) is matched with gaps)
        if s1 == '' or s2 == '':
            sub_solns[key] = max(len(s1), len(s2))
            return max(len(s1), len(s2))

        # either the optimal alignment comes when both last chars in string are matched
        # or if last char of either word is matched with a gap in the other, calculate
        # the 3 sub-problems recursively and choose the minimum
        match_sol = (int(s1[-1] == s2[-1]) + 1) % 2  # 1 if last chars are diff, 0 if same
        matchkey = 'w1{0}w2{1}'.format(s1[:-1], s2[:-1])
        if matchkey in sub_solns:
            match_sol += sub_solns[matchkey]
        else:
            match_sol += find_opt_score(s1[:-1], s2[:-1])

        gap_sol1 = 1
        gapkey1 = 'w1{0}w2{1}'.format(s1[:-1], s2)
        if gapkey1 in sub_solns:
            gap_sol1 += sub_solns[gapkey1]
        else:
            gap_sol1 += find_opt_score(s1[:-1], s2)

        gap_sol2 = 1
        gapkey2 = 'w1{0}w2{1}'.format(s1, s2[:-1])
        if gapkey2 in sub_solns:
            gap_sol2 += sub_solns[gapkey2]
        else:
            gap_sol2 += find_opt_score(s1, s2[:-1])


        sub_solns[key] = min(match_sol, gap_sol1, gap_sol2)
        return min(match_sol, gap_sol1, gap_sol2)

    opt_score = find_opt_score(S1, S2)

    # back-track to reconstruct actual alignment of strings (can be ambiguous, will find one)
    S1_opt = ''
    S2_opt = ''
    s1 = S1
    s2 = S2
    while len(s1) > 0 and len(s2) > 0:
        # we've already filled in sub-problems in dict, will always have valid keys to check
        key = 'w1{0}w2{1}'.format(s1, s2)
        score = sub_solns[key]

        matchkey = 'w1{0}w2{1}'.format(s1[:-1], s2[:-1])
        matchcase = sub_solns[matchkey] + (int(s1[-1] == s2[-1]) + 1) % 2
        if matchcase == score:
            S1_opt += s1[-1]
            S2_opt += s2[-1]
            s1 = s1[:-1]
            s2 = s2[:-1]
            continue

        gapkey1 = 'w1{0}w2{1}'.format(s1[:-1], s2)
        gap1case = sub_solns[gapkey1] + 1
        if gap1case == score:
            S1_opt += s1[-1]
            S2_opt += '-'  # gap
            s1 = s1[:-1]
            continue

        # don't even need to check gapcase2, if alignment didn't come from matching the last
        # chars or matching the last char of s1 with a gap, it had to come from last case
        S1_opt += '-'  # gap
        S2_opt += s2[-1]
        s2 = s2[:-1]

    # loop ends when at least one string is empty. if both empty, we're done
    # otherwise if one is non-empty, the other must be empty by this condition
    # and we match remaining word with gaps, add len(non-empty word) gaps to other word
    if len(s1) > 0:
        S1_opt = s1 + S1_opt[::-1]
        S2_opt = '-'*len(s1) + S2_opt[::-1]
    elif len(s2) > 0:
        S1_opt = '-'*len(s2) + S1_opt[::-1]
        S2_opt = s2 + S2_opt[::-1]
    else:
        S1_opt = S1_opt[::-1]
        S2_opt = S2_opt[::-1]

    # we're done, report our findings
    print('\n The maximal alignment of strings {0} and {1} has a minimal'.format(S1, S2),
           'penalty score of {0}.'.format(opt_score))
    print('\n One possible maximal alignment is given by the strings {0}, {1}'.format(S1_opt, S2_opt))


if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()

    print('\n This code ran in {0:6f} seconds.\n'.format(t1 - t0))

    raise SystemExit
