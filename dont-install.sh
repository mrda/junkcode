#!/bin/bash
#
# dont-install-sh - This is not the install script you're looking for
#                   Derived from https://xkcd.com/1654/
#
echo "You really don't want to do this"
exit 1
pip install "$1" &
easy_install "$1" &
brew install "$1" &
npm install "$1" &
yum install "$1" &
dnf install "$1" &
docker run "$1" &
pkg install "$1" &
apt-get install "$1" &
git clone https://github.com/"$1"/"$1" && cd "$1" && ./configure && make && \
make install
curl "$1" | bash &
