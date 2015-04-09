#!/usr/bin/env python
#
# monkey_patching_decorators.py - example code on how to monkey patch a
#                                 python decorator. This was too hard to
#                                 work out when I needed it not to save
#                                 it for later :)
#
#                                 Just import this file along with the
#                                 original file with the decorator,
#                                 remembering that decorators are applied
#                                 at function definition time, but invocation
#                                 time (except for nested functions)
#
# Copyright (C) 2015 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# Or try here: http://www.fsf.org/copyleft/gpl.html
#

# Or any other package with a decorator you need to monkey patch
import wsmeext.pecan as wsme_pecan

original_decorator = wsme_pecan.wsexpose  # wsexpose is the decorator to patch


def my_decorator(*args, **kwargs):
    # Do what you need to do, like add things to kwargs
    kwargs['rest_content_types'] = "('json',)"
    # Invoke the original decorator
    return original_decorator(*args, **kwargs)

# Now make all callers believe they are calling the original decorator
# where instead they are calling your local function, which calls the
# original one
wsme_pecan.wsexpose = my_decorator
