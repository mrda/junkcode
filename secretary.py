#!/usr/bin/env python
#
# secretary.py - Solve the secretary problem.  How to find the
# optimal value in a list, trying not to examine every single value
#
# Copyright (C) 2015 Michael Davies <michael@the-davies>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
import math
import random
import sys


debug = False


def _find_best_position(data):
    """ Find the largest value, and it's index in the array """
    largest = 0
    largest_idx = -1
    for idx, val in enumerate(data):
        if val > largest:
            largest = val
            largest_idx = idx
    return largest_idx+1, largest


def _greaterthan(a, b):
    """ Simple '>' function """
    return a > b


def guess_best_secretary(sample_size, get_next_candidate_fn,
                         score_candidate_fn):
    """ Provide a solution for the 'Secretary Problem'
    See http://en.wikipedia.org/wiki/Secretary_problem
    """

    # Find the highest value in the first stop_point
    # elements
    stop_point = int(sample_size / math.e)

    candidate_idx = 0
    best_candidate_score = 0
    for i in xrange(1, stop_point):
        next_candidate = get_next_candidate_fn()
        candidate_score = score_candidate_fn(next_candidate)
        if candidate_score > best_candidate_score:
            candidate_idx = i
            best_candidate_score = candidate_score
    if debug:
        print ("First pass up to N/e, we found best value %s in pos %s" %
               (best_candidate_score, candidate_idx))

    # Find the first value, after the stop_point, which
    # is higher than those examined already
    best_candidate_idx = 0
    for j in xrange(stop_point, sample_size+1):
        candidate = get_next_candidate_fn()
        candidate_score = score_candidate_fn(candidate)
        if candidate_score > best_candidate_score:
            best_candidate_idx = j
            best_candidate_score = candidate_score
            break
        elif j == sample_size:
            # There were none better, we have to choose the last applicant
            if debug:
                print ("*** Rats! We have to choose the last applicant")
            best_candidate_idx = sample_size
            best_candidate_score = candidate_score

    return best_candidate_idx, best_candidate_score


if __name__ == '__main__':

    class TestData:
        def __init__(self):
            self.data = random.sample(range(1, 10000000), 1000000)
            self.current_idx = 0

        def get_next_candidate(self):
            d = self.data[self.current_idx]
            self.current_idx += 1
            return d

        def score_candidate(self, c):
            return c

        def get_size(self):
            return len(self.data)

    print("Solving the Secretary problem...")
    test_data = TestData()
    pos, value = guess_best_secretary(test_data.get_size(),
                                      test_data.get_next_candidate,
                                      test_data.score_candidate)
    print("The value chosen was %s in position %s" % (value, pos))
    print("We searched %-2d%% of all possible values" %
          (pos/float(test_data.get_size())*100))

    best_pos, best_value = _find_best_position(test_data.data)
    print("(The actual best value was %s in position %s)" %
          (best_value, best_pos))
    if best_value == value:
        print ("\o/ Yay we guessed correctly!")

    if debug:
        for i in range(0, len(test_data.data)):
            print(i+1, test_data.data[i])
