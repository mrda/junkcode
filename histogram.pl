#!/usr/bin/perl
#
# Histogram library and command-line tool - generate and print a histogram
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

=head1 NAME

MRDA::Histogram - Do some simple histogram analysis of supplied data

=head1 SYNOPSIS

use MRDA::Histogram qw( build_histogram print_histogram );
my $histogram = build_histogram(\@input_array);
print_histogram($histogram);

or

./histogram.pl file-of-data.txt

or

./histogram.pl
<insert data here, one item per line>
^D

=head1 DESCRIPTION

Build a simple histogram of supplied data, identify the least/most frequent entries and
the number of items examined.  Can be invoked from the command-line, or included as a
Perl library.

This is a very quick and dirty script, if you want anything bigger and better, go
to CPAN.

=head1 BUGS AND LIMITATIONS

  None known

=cut

package MRDA::Histogram;

use vars qw( @EXPORT_OK );
use base qw ( Exporter );
our @EXPORT_OK = qw( build_histogram print_histogram );

use strict;
use warnings;

# Invoke as command-line if required
__PACKAGE__->main() unless caller;

#
# main() - only run if this file is invoked as a commandline script
#
sub main {
    my @input;

    while (my $line = <>) {
        chomp $line;
        next if $line eq "";
        push @input, $line;
    }

    my $hist_ref = build_histogram(\@input);
    print_histogram($hist_ref);
}


=head2 build_histogram

=head3 SYNOPSIS

  use MRDA::Histogram qw( build_histogram print_histogram );
  my $histogram = build_histogram(\@input_array);
  print_histogram($histogram);

=head3 DESCRIPTION

  Build a hash of analysed data, including information required to display a simple
  textual histogram.

=head3 DIAGNOSTICS

  None

=head3 SEE ALSO

  print_histogram

=cut

sub build_histogram {

    my $arrref = shift;

    my @arr = @$arrref;
    my $len = scalar(@arr);

    my %freq_table = ();

    for (my $i = 0; $i < $len; $i++) {
        if (exists $freq_table{$arr[$i]}) {
            $freq_table{$arr[$i]} = $freq_table{$arr[$i]} + 1;
        } else {
            $freq_table{$arr[$i]} = 1;
        }
    } # for

    # Analyse and print
    my $least_elem;
    my $most_elem;
    my $least_elem_number;
    my $most_elem_number;
    my $mean_occurances = 0;
    my $total_occurances = 0;

    my $key;
    my $val;

    foreach my $key (sort {$freq_table{$a} cmp $freq_table{$b} } keys %freq_table) {
        # Find the least/most occuring elements
        if ( (not defined $least_elem) ||
             ($freq_table{$key} <  $least_elem_number) ) {
             $least_elem = $key;
             $least_elem_number = $freq_table{$key};
        } elsif ( (not defined $most_elem) ||
             ($freq_table{$key} >  $most_elem_number) ) {
             $most_elem = $key;
             $most_elem_number = $freq_table{$key};
        }
        # Running total
        $total_occurances += $freq_table{$key};
    }

    my %results = ();
    $results{'histogram'} = \%freq_table;
    $results{'least'} = $least_elem;
    $results{'least_num'} = $least_elem_number;
    $results{'most'} = $most_elem;
    $results{'most_num'} = $most_elem_number;
    $results{'total'} = $total_occurances;

    return \%results;
}

=head2 print_histogram

=head3 SYNOPSIS

  use MRDA::Histogram qw( build_histogram print_histogram );
  my $histogram = build_histogram(\@input_array);
  print_histogram($histogram);

=head3 DESCRIPTION

  Print out a textual representation of a histogram, given a hash previously built by
  build_histogram.

=head3 DIAGNOSTICS

  None

=head3 SEE ALSO

  build_histogram

=cut

sub print_histogram {

    my $hashref = shift;

    my %hash = %$hashref;
    my $hist_ref = $hash{'histogram'};
    my %hist = %$hist_ref;

    while ( my ($key, $val) = each(%hist) ) {
        print $key . ' ' . '#' x $hist{$key} . "\n";
    } # while

    print "There was a total of $hash{'total'} data points analysed\n";
    print "The least occuring element was \"$hash{'least'}\" with $hash{'least_num'} occurances\n";
    print "The most occuring element was \"$hash{'most'}\" with $hash{'most_num'} occurances\n";
}

# So long and thanks for all the fish!
1;
