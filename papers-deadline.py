#!/usr/bin/env python
#
# papers-deadline.py - print out useful stuff to nag the linux.conf.au
#                      papers committee
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
#

import datetime
import math

####### START OF THINGS TO UPDATE #########
NUM_MINICONFS = 1
NUM_PRESENTATIONS = 1
NUM_PROTOTYPES = 1
NUM_TUTORIALS = 1
REVIEW_CLOSE = '23/08/2015'
######### END OF THINGS TO UPDATE #########

date_format = '%d/%m/%Y'

total_number = (NUM_MINICONFS + NUM_PRESENTATIONS + NUM_PROTOTYPES +
                NUM_TUTORIALS)

today = datetime.date.today()
close_date = datetime.datetime.strptime(REVIEW_CLOSE, date_format).date()
days_left = (close_date - today).days

print('There are %s miniconfs to review' % NUM_MINICONFS)
print('There are %s presentations to review' % NUM_PRESENTATIONS)
print('There are %s prototypes to review' % NUM_PROTOTYPES)
print('There are %s tutorials to review' % NUM_TUTORIALS)

print('\nFor a TOTAL of %s things to review\n' % total_number)

print('<<< REVIEWING CLOSES IN %d DAYS >>>\n' % days_left)

for i in [25, 50, 100]:
    print('If you wanted to review %d%% you need to do %d per day' %
          (i, math.ceil(total_number * i / (days_left * 100.0))))
