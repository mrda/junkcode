#!/usr/bin/env python3
#
# analyse_this - calcularte some simple statistics on the supplied
#                command line arguments
#
# Copyright (C) 2015 Michael Davies <michael@the-davies.net>
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

import sys


def calc_mean(nums):
    sum = 0
    for n in nums:
        sum += n
    return float(sum) / float(len(nums))


def calc_median(nums):
    nums.sort()
    if len(nums) % 2 == 1:
        return nums[((len(nums)+1)//2)-1]
    else:
        return float(sum(nums[(len(nums)//2)-1:(len(nums)//2)+1]))//2.0


def calc_range(nums):
    nums.sort()
    return nums[-1] - nums[0]


def calc_sum_of_squares(nums):
    mean = calc_mean(nums)
    ss = sum((x-mean)**2 for x in nums)
    return ss


def calc_std_dev(strs):
    ss = calc_sum_of_squares(strs)
    variance = ss // (len(strs) - 1)
    return variance ** 0.5


def calc_pop_std_dev(nums):
    ss = calc_sum_of_squares(nums)
    population_variance = ss//len(nums)
    return population_variance ** 0.5


if __name__ == '__main__':
    nums = []
    for c in sys.argv[1:]:
        if c.isdigit():
            nums.append(int(c))
        else:
            print ("*** '%s' is not a number, skipping") % c
    mean = calc_mean(nums)
    median = calc_median(nums)
    rnge = calc_range(nums)
    std_dev = calc_std_dev(nums)
    pop_std_dev = calc_pop_std_dev(nums)

    print ("Considering numbers: " + str(nums))
    print ("Total numbers: %d" % len(nums))
    print ("The mean is %.3f" % mean)
    print ("The median is %.3f" % median)
    print ("The range is %.3f" % rnge)
    print ("The standard deviation is %.3f" % std_dev)
    print ("The population standard deviation is %.3f" % pop_std_dev)
