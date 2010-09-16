#!/usr/bin/perl
#
# Sample code for dealing with:
# 1) Big numbers and going back and forth to hex strings
# 2) Generating HMAC-MD5's for various data sets
#
# (C) Copyright 2010 Michael Davies <michael@the-davies.net>
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
use warnings;
use strict;
use bignum;
use Digest::HMAC_MD5 qw( hmac_md5_hex hmac_md5 );

# Converting hex strings to/from big numbers
sub hexstr_to_num {
    my $hexstr = shift;
    return hex $hexstr;
}

sub num_to_hexstr {
    my $num = shift;
    return $num->as_hex;
}

sub test_conversion {
    my $title = shift;
    my $number = shift;
    my $expected_hexstr = shift;
    print $title . "\n";
    print "Testing number: $number\n";
    my $hexstr = num_to_hexstr($number);
    print "...which is hex string: $hexstr\n";
    if ($hexstr eq $expected_hexstr) {
        print "...... and it matches what we expect\n";
    } else {
        print "****** FAIL - mismatch!\n";
    }
    my $converted_number = hexstr_to_num($hexstr);
    print "...which is number: $converted_number\n";
    if ($converted_number == $number) {
        print "...... and it matches what we expect\n";
    } else {
        print "****** FAIL - mismatch!\n";
    }
    print "\n";

}

test_conversion("Test Case HexStr<->Num 1", 12, "0xc");
test_conversion("Test Case HexStr<->Num 2", 42405, "0xa5a5");
test_conversion("Test Case HexStr<->Num 3", 3735928559, "0xdeadbeef");
test_conversion("Test Case HexStr<->Num 4", 43350435543668877756353850967874637398866555766, "0x797e69837da10bf3bd0095c1be7493c65b27376");

# HMAC-MD5 test
sub test_hmac_md5 {
    my $title = shift;
    my $data = shift;
    my $secret = shift;
    my $expected = shift;

    my $digest = hmac_md5_hex($data, $secret);

    print $title . "\n";
    print "Expected:   " . $expected->as_hex. "\n";
    print "Calculated: 0x" . $digest . "\n\n";
}


# Test cases - refer http://tools.ietf.org/html/rfc2104
test_hmac_md5("Test Case HMAC-MD5 1", "Hi There", pack("H*", '0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b'), 0x9294727a3638bb1c13f48ef8158bfc9d);
test_hmac_md5("Test Case HMAC-MD5 2", "what do ya want for nothing?", "Jefe", 0x750c783e6ab0b503eaa86e310a5db738);
test_hmac_md5("Test Case HMAC-MD5 3",
              pack("H*", 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'),
              pack("H*", 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'), 0x56be34521d144c88dbb8c733f0e8b3f6);


