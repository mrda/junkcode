#!/usr/bin/env python
#
# circleplot.py - plot circles looking for intersecting points
#
# Copyright (C) 2019 Michael Davies <michael@the-davies.net>
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
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

axes = [x for x in range(-12, 12)]
plt.xticks(axes)
plt.yticks(axes)
ax.grid(True)

ax.add_patch(plt.Circle((5, 5), 5, color='#FF6347', alpha=0.7))
ax.add_patch(plt.Circle((0, 0), 5, color='#002366', alpha=0.7))

ax.set_aspect('equal', adjustable='box-forced')
ax.plot()

print()
print('Press \'q\' to exit in the matplotlib window...')
print()
plt.show()
