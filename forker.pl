#!/usr/bin/perl
#
# Standard Perl fork template
#
# Copyright (C) 2012 Michael Davies <michael@the-davies.net>
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
use strict;
use warnings;
use Readonly;
use Carp qw(carp confess);
use Time::HiRes qw(usleep);
use POSIX qw(:sys_wait_h);

Readonly my $CHILD_REAPER_DELAY_MICRO   => 100_000;      # Micro Seconds
Readonly my $CHILD_REAPER_WARNING_DELAY => 1800;         # Seconds

my $debug = 1;
my $num_children = 5; # How many workers should we have?

# Parents should be responsible and keep track of their children.
my %global_child_worker_procs;

#
# Child worker
#
sub start_worker {
    # Do stuff - this is the worker code for each child
    my $worker_num = shift;

    print "I am worker $worker_num, starting up...\n" if $debug;

    # <<< insert real work here >>>
    sleep(10); # Fake some work :)
    # <<< end of insert real work here >>>

    print "Worker $worker_num is going away now\n" if $debug;

} ## end sub start_worker

sub reaper {
    my $stiff;
    my $timeout = time() + $CHILD_REAPER_WARNING_DELAY;
    while ( ( $stiff = waitpid( -1, &WNOHANG ) ) > 0 ) {
        usleep($CHILD_REAPER_DELAY_MICRO);
        my $current_time = time();
        if ( $current_time > $timeout ) {
            print "Failed to reap child within $CHILD_REAPER_WARNING_DELAY seconds\n" if $debug;
            last;
        } ## end if
    } ## end while
    return;
} ## end sub reaper

sub kill_children {
    # Ask my children to TERMinate
    foreach my $child_pid ( keys %global_child_worker_procs ) {
        if ($debug) {
            print STDERR "Terminating child worker process $child_pid and exiting.\n";
        }
        if ( kill( 'TERM', $child_pid ) ) {
            delete $global_child_worker_procs{$child_pid};
        }
    }
    # Hard KILL any that are left.  Sometimes you have to be cruel to be kind.
    if ( keys %global_child_worker_procs ) {
        sleep(10);
        foreach my $child_pid ( keys %global_child_worker_procs ) {
            kill( 'KILL', $child_pid );
        } # end foreach
    } ## end if
    exit 0;
} ## end sub kill_children

sub start_worker_wrapper {
    my $worker_num = shift;

    my $pid = fork();
    if ( $pid == 0 ) {
        # child
        start_worker( $worker_num );
    } elsif ( $pid > 0 ) {
        # parent
        $global_child_worker_procs{$pid} = $worker_num;
        if ( $debug ) {
            print STDERR "Started worker process number $worker_num with process id $pid\n";
        }
    } else {
        # failure
        confess "Can't fork() to start worker process number $worker_num because $!";
    }
    return $pid;
} ## end sub start_worker_wrapper

sub main {
    print "Parent: My pid is $$\n" if $debug;

    # Make sure dead children don't accumulate
    $SIG{CHLD} = \&reaper;

    foreach my $worker_number ( 1 .. $num_children ) {
        # If we're the child, don't continue executing the loop
        # we don't want a geometric progression happening :)
        exit if not start_worker_wrapper( $worker_number ); 
    }

    # Make sure we kill the children if we're going to die
    $SIG{INT}  = \&kill_children;
    $SIG{HUP}  = \&kill_children;
    $SIG{ABRT} = \&kill_children;
    $SIG{TERM} = \&kill_children;
    $SIG{QUIT} = \&kill_children;

    print "All the children have been forked.  Kill me with ^C\n" if $debug;
    while (1) {
        print "Parent: Kill me, and any children I've misplaced, with ^C\n" if $debug;
        sleep(60);
    } #end while

} # end sub main

# Let's run this thang
main();

