#!/usr/bin/env perl
#
# onchange - file1 file2 ... fileN command
#
# Run "command" if any of file* changes
#  e.g. onchange.pl dir 'clear; prove -rv'
#  e.g. onchange.pl dir 'clear; make; make test'
#
# Lifted from "Perl Hacks" by chromatic, Damian Conway abd Curtis 'Ovid' Poe.
# Copyright 2006 O'Reilly Media, Inc., 0-596-52674-1.
# Hack #63 - modified by Michael Davies <michael@the-davies.net>
#
# Revision Hostory
# v1.0 09/07/2008 - Initial hacked version
#
# 80 char marker
# 234567890123456789012345678901234567890123456789012345678901234567890123456789
#
use strict;
use warnings;

use File::Find;
use Digest::MD5;

my $command     = pop @ARGV;
my $files       = [@ARGV];
my $last_digest = '';

# Regular expressions of files that we don't care about
# Notably editor save files - vim, emacs, etc and svn dirs
my @exclusions = ( qr/^.*?.swp$/ , qr/^#.*?#$/, qr/^\.svn$/ );

sub has_changed {
    my $files  = shift;
    my $md5 = Digest::MD5->new();

    # Nasty perl code.  Here be dragons.
    find( sub { $md5->add( $File::Find::name, ( stat($_) )[9] )
        if ! grep { $File::Find::name =~ $_  } @exclusions },
            grep { -e $_ } @$files );

    my $hash = $md5->digest();
    my $has_changed = $hash ne $last_digest;
    $last_digest = $hash;

    return $has_changed;
}

# Growl Support on Mac OS X, depends on Growl being installed
my $growlmsg;
my $growlify = 0;
if ( -x '/usr/local/bin/growlnotify' ) {
    $command .= "; ";
    $command .= "/usr/local/bin/growlnotify -t 'onchange.pl reports...' -m 'Files changed and scripts run'";
}

while (1) {
    system( $command ) if has_changed( $files );
    sleep 1;
}


