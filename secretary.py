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


def _find_best_position(data):
    """ Find the largest value, and it's index in the array """
    largest = 0
    largest_idx = -1
    for idx, val in enumerate(data):
        if val > largest:
            largest = val
            largest_idx = idx
    return largest_idx, largest


def _greaterthan(a, b):
    """ Simple '>' function """
    return a > b


def guess_best_secretary(data, evaluate_fn):
    """ Provide a solution for the 'Secretary Problem'
    See http://en.wikipedia.org/wiki/Secretary_problem
    """

    # Find the highest value in the first stop_point
    # elements
    stop_point = int(len(data) / math.e)
    best_val = 0
    best_idx = 0
    for i in range(1, stop_point):
        if evaluate_fn(data[i], best_val):
            best_idx = i
            best_val = data[i]

    # Find the first value, after the stop_point, which
    # is higher than those examined already
    best_applicant_idx = 0
    best_applicant_val = 0
    for j in range(stop_point+1, len(data)-1):
        if evaluate_fn(data[j], best_val):
            best_applicant_idx = j
            best_applicant_val = data[j]

    # There were none better, chose the last applicant
    if best_applicant_idx == 0:
        print ("*** Rats! We have to choose the last applicant")
        best_applicant_idx = len(data)
        best_applicant_val = data[len(data)-1]

    return best_applicant_idx, best_applicant_val


if __name__ == '__main__':

    if len(sys.argv) != 1:
        # Assume params are an ordered list of numbers you want to process
        data = sys.argv[1:]
        test = False
    else:
        # Run some tests, since no data provided
        data = random.sample(range(1, 10000), 5000)
        test = True

    print("Solving the Secretary problem...")
    pos, value = guess_best_secretary(data, _greaterthan)
    print("The value chosen was %s in position %s" % (value, pos))
    print("We searched %-2d%% of all possible values" %
          (pos/float(len(data))*100))

    if test:
        best_pos, best_value = _find_best_position(data)
        print("(The actual best value was %s in position %s)" %
              (best_value, best_pos))
        if best_value == value:
            print ("\o/ Yay we got it right!")
