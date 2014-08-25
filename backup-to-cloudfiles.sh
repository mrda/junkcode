#!/bin/sh
HOSTN=$(hostname | cut -f 1 -d'.')
cd ${HOME}
for item in photos video
do
  ${HOME}/src/cloudfiles-tools/push_to_cloudfiles.py file://$item ord://backup/${HOSTN}/$item
done
