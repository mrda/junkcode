#!/usr/bin/env bash
#
# Clone all the openshift repositories, locally.
# Original version by tony@bakeyournoodle.com
#
# Copyright (C) 2021 Michael Davies <michael@the-davies.net>
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

_check_cmd_avail ()
{
    if ! hash ${1} &> /dev/null; then
        echo "The required command '$1' could not be found, exiting"
        exit 1
    fi
}
_check_cmd_avail curl
_check_cmd_avail git
_check_cmd_avail jq

CDPATH=

USAGE="Usage: $(basename $0) [-h|--help|--refresh]"

while [ $# -gt 0 ] ; do
    case "$1" in
    --help|-h)
        echo $USAGE
        echo "Clone all the OpenShift respoitories into the current directory"
        exit 0
        ;;
    --refresh)
        REFRESH=1
        shift
        ;;
    *)
        echo $USAGE
        echo "Unknown option specified"
        exit 1
        ;;
    esac
done

if [ "${REFRESH:=0}" -eq 1 -o ! -e .repos ] ; then
    # Get the number of pages via the link header in the server resonse
    TMP_HEAD_FILE=$(mktemp --tmpdir=. .cache.head.XXXXXXXXX)
    curl --head \
         -H 'Accept: application/vnd.github.v3+json' \
        'https://api.github.com/orgs/openshift/repos?type=public&page_size=100&page=1' \
        --dump-header "$TMP_HEAD_FILE"
    _max=$(awk -F\, '/^link:/ {print $NF}' "$TMP_HEAD_FILE" | sed -ne 's/^.*page=\([0-9]*\).*$/\1/p')
    /bin/rm "$TMP_HEAD_FILE"

    # For grab all the json pages
    TMP_DATA_FILE=$(mktemp --tmpdir=. .cache.json.XXXXXXXXX)
    for page in $(seq 1 $_max) ; do
        curl --silent \
          -H 'Accept: application/vnd.github.v3+json' \
          "https://api.github.com/orgs/openshift/repos?type=public&page_size=100&page=$page" \
          --output "$TMP_DATA_FILE.$page"
    done

    # Grab just the repo clone URLs
    jq -r '.[].clone_url' "$TMP_DATA_FILE".[0-9]* > .repos
    /bin/rm "$TMP_HEAD_FILE" "$TMP_DATA_FILE".[0-9]*
fi

for url in $(sort .repos) ; do
    dir=$(basename $url .git)
    if [ ! -d "$dir" ] ; then
        echo Cloning $dir
        git clone "$url" >/dev/null 2>&1
    else
        echo Updating $dir
        cd $dir
        git remote update >/dev/null 2>&1
        cd - >/dev/null
    fi
done
