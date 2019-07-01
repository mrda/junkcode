#!/usr/bin/env getpy3.sh
#
# ha-list-entities.py - List all the available entities from Home Assistant
#                       Depends the following environment variables:
#                         * HA_BASE_URL - where to find Home Assistant
#                         * HA_TOKEN - a long-lived auth token
#                       But if they aren't define, it'll try and read them
#                       from $HOME/.ha.sh
#
#                       For example:
#                         HA_BASE_URL="http://192.168.0.1:8123"
#                         HA_TOKEN="dfgjk76dghdfg68dfghjk...j35k345"
#
# Copyright (C) 2019 Michael Davies <michael@the-davies.net>
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
import configparser
import simplejson
import requests
import sys
import os


def dequote(string):
    """Unquotify a string if it starts/ends with eith er a ' or " """
    if (string[0] == string[-1]) and string.startswith(("'", '"')):
        return string[1:-1]
    return string


def get_data(authfile, urlpath):
    """Do an HTTP GET to retrieve home assistant data"""

    # The base URL and authentication token can be either in the
    # environment, or in a file.  Either way, we need to retrieve this
    # information from somewhere.  Fail otherwise.
    HA_BASE_URL_ORIG = HA_BASE_URL = 'HA_BASE_URL'
    HA_TOKEN_ORIG = HA_TOKEN = 'HA_TOKEN'
    if HA_BASE_URL in os.environ and HA_TOKEN in os.environ:
        HA_BASE_URL = os.environ[HA_BASE_URL]
        HA_TOKEN = os.environ[HA_TOKEN]
    else:
        cp = configparser.ConfigParser()
        with open(authfile) as stream:
            cp.read_string("[top]\n" + stream.read())
        HA_BASE_URL = dequote(cp['top'][HA_BASE_URL])
        HA_TOKEN = dequote(cp['top'][HA_TOKEN])
    if HA_BASE_URL == HA_BASE_URL_ORIG or HA_TOKEN == HA_TOKEN_ORIG:
        exit("HA_BASE_URL and HA_TOKEN must be defined in your environment")

    url = HA_BASE_URL + urlpath
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + HA_TOKEN}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        sys.exit("Error connecting to '{}'. HTTP error code is {}".
                 format(urlpath, r.status_code))

    return r.content


auth_file = os.environ['HOME'] + "/.ha.sh"
api_path = "/api/states"
content = get_data(auth_file, api_path)
array = simplejson.loads(content)

for element in array:
    if 'entity_id' in element:
        print(element['entity_id'])
