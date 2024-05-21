#!/usr/bin/env python
#
# calc-return.py Calculate the annualised return of an investment.
#
# Copyright (C) 2024 Michael Davies <michael@the-davies.net>
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

def get_date(prompt):
    no_date = True
    while no_date:
        try:
            d = input(prompt)
            if d == 'today':
                parsed_date = datetime.datetime.now()
            else:
                parsed_date = datetime.datetime.strptime(d, "%d/%m/%Y")
            no_date = False
        except ValueError:
            print("Sorry, wrong date format. Try again.")
    return parsed_date

start_date = get_date("Enter starting date (dd/mm/yyyy): ")
end_date = get_date("Enter ending date (dd/mm/yy or today): ")

# Flip the dates for user error
if start_date > end_date:
    start_date, end_date = end_date, start_date
delta = end_date - start_date

tot = float(input("Enter total return (0.3 = 30%): "))
annual_return = ((1 + tot)**(365/delta.days)) - 1

print(f"Time period is {delta.days} days, which is {delta.days/365:.2f} years")
print(f"Annualised return is {(annual_return*100):.2f}%")

