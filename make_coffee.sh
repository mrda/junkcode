#!/bin/sh

# make_coffee.sh
# Revision $Revision: 1.7 $
# Last Modified $Date:
# 1999/10/14 03:05:20 $

cat /dev/tap \
| heater \
| coffee_filter \
> /dev/mug
