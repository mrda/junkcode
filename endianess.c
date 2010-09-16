/*
 * endianness - Determine if we are running on a little or big
 * endian machine.
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

int main(int argc, char* argv[]) {

    unsigned int data = 0x01234567;
    char* data_ptr = (char*)&data;

    /* big endian check: 0x01 0x23 0x45 0x67 */
    if ((data_ptr[0] == 0x01)
            && (data_ptr[1] == 0x23)
            && (data_ptr[2] == 0x45)
            && (data_ptr[3] == 0x67)) {
            printf("I'm big endian\n");

    /* little endian check:  0x67 0x45 0x23 0x01 */
    } else if ((data_ptr[0] == 0x67)
            && (data_ptr[1] == 0x45)
            && (data_ptr[2] == 0x23)
            && (data_ptr[3] == 0x01)) {
            printf("I'm little endian\n");

    } else {
            /* Unknown endianess :-( */
            printf("I'm confused about my endianess :-(\n");
    }

    return 0;

}
