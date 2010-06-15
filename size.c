/*
 * size - Find out the size of the standard C data types
 * (up until 16 bytes)
 *
 * Copyright (C) 2004 Michael Davies <michael@the-davies.net>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
 * 02111-1307, USA.
 *
 */
#include <stdio.h>

void find_size(int size)
{
        int found = 0;

        if (size == sizeof(int)) {
                printf("%d bytes is a int\n", size);
                found = 1;
        }

        if (size == sizeof(short)) {
                printf("%d bytes is a short\n", size);
                found = 1;
        }

        if (size == sizeof(char)) {
                printf("%d bytes is a char\n", size);
                found = 1;
        }

        if (size == sizeof(long)) {
                printf("%d bytes is a long\n", size);
                found = 1;
        }

        if (size == sizeof(long long)) {
                printf("%d bytes is a long long\n", size);
                found = 1;
        }

        if (size == sizeof(double)) {
                printf("%d bytes is a double\n", size);
                found = 1;
        }

//        if (!found) {
//                printf("%d bytes is not used.\n", size);
//        }
}

int main(int argc, char **argv)
{
        int i;

        for (i=1; i<=16; i++) {
                find_size(i);
        }
        return 0;
}

