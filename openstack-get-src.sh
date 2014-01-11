#!/bin/bash
#
# openstack-get-src.sh - grab all the openstack code from github
#                        so you can hack on all the things while
#                        traveling on a plane :)
#
# Original author unknown
#
USERNAME="mrda"

for repo in `ssh review.openstack.org gerrit ls-projects` ; do
    mkdir -p $(dirname $repo)
    if [ ! -d $repo ] ; then
        echo "Cloning $repo"
        git clone git://git.openstack.org/$repo $repo
        (cd $repo; git review -s)
    else
        echo "Updating $repo"
        (cd $repo; git remote update)
    fi
done

