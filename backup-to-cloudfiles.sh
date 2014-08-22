#!/bin/sh
cd ${HOME}
for item in photos
do
  ${HOME}/src/cloudfiles-tools/push_to_cloudfiles.py file://$item ord://backup/${HOSTNAME}/$item
done
