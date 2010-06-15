/* ttylock - manipulate and lock the screen via curses
 *
 * Copyright (C) 1990, 2004, 2005 Michael Davies <michael@the-davies.net>
 *
 * Compile with: gcc -Wall -pedantic -lncurses -lpam -lpam_misc ttylock.c
 * Known to compile on: Linux shadowfax 2.6.8.1.i386-inotify-1 #1 Sun Nov 21 00:10:51 CST 2004 i686 GNU/Linux (uname -a)
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 * Or try here: http://www.fsf.org/copyleft/gpl.html
 */

#include <string.h>
#include <signal.h>
#include <curses.h>

#define LEN 80
#define BACKDOOR "frobnitz" /* Just make sure BACKDOOR less than LEN chars */
#define DEBUG 0

int main (int argc, char* argv[])
{
    char password[LEN+1];
    int  pigs_can_fly = 1;

    /* Catch what we can, pretend that SIGKILL is catchable */
    if (DEBUG != 1)
    {
        signal(SIGHUP,  SIG_IGN);
        signal(SIGINT,  SIG_IGN);
        signal(SIGQUIT, SIG_IGN);
        signal(SIGKILL, SIG_IGN);
        signal(SIGTERM, SIG_IGN);
        signal(SIGTSTP, SIG_IGN);
    }

    /* Initialise Curses */
    initscr();

    /* Let me process everything, and turn off auto echo */
    raw(); 
    if (DEBUG != 1)
    {
        noecho();
    }

    while (pigs_can_fly) {

        /* printf won't work due to noecho() */
        printw("Password:");

        getnstr(password, LEN);

        if (strncmp(BACKDOOR, password, strlen(BACKDOOR)) == 0) {
            pigs_can_fly = 0; /* Match */
        } else {
            printw("Without the password, you're going nowhere :-)\n");
        }
    }

    /* Turn echo'ing back on, and leave raw mode */
    if (DEBUG != 1)
    {
        echo();
    }
    noraw();

    /* Cleanup from curses */
    endwin();

    return 0;
}

