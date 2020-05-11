#
# Michael's bash profile/aliases
#
# Copyright (C) 1989-2019 Michael Davies <michael@the-davies.net>
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

# Check for things existing
__command_exists ()
{
    hash ${1} &> /dev/null
    return $?
}

# OS Detection
PLATFORM='unknown'
case "$OSTYPE" in
  solaris*)
    PLATFORM="SOLARIS";;
  darwin*)
    PLATFORM="OSX";;
  linux*)
    PLATFORM="LINUX";;
  bsd*)
    PLATFORM="BSD";;
  *)
    PLATFORM='unknown'
esac
export PLATFORM

# Linux distro detection
DISTRO='unknown'
if [[ "z${PLATFORM}" == "zLINUX" ]]; then
    if __command_exists lsb_release; then
        DISTRO=$(lsb_release -i | cut -f2)
    fi
fi

# Shell things
export EDITOR=vim
export VISUAL=vim
#No longer needed export ACK_OPTIONS="--color" # so we get color
export CDPATH=.:~:~/src

# Take control of your history
export HISTCONTROL="ignoreboth"
export HISTTIMEFORMAT="[%F %T] "
export HISTSIZE=-1
export HISTFILESIZE=-1
shopt -s histappend

# Deal with Centos 7 being broken
if [[ "z${DISTRO}" == "zCentOS" ]]; then
    unset LESS
    unset LESSOPEN
else
    export LESS="-R" # so we get colour  # Breaks on Centos 7
    export LESSOPEN='|pygmentize -g %s'  # Breaks on Centos 7
fi

alias l="ls -la $@"  # args quoted
alias cls="clear"
alias tac="perl -e 'print reverse <> '"
alias catdata="perl -ne 's/^#.*//; print if /\S/'"
function mkcd() { mkdir -p "$@" && cd "$@"; } && alias mkcda=mkcd

# Cheatsheet from the comand-line
function cs() { curl cheat.sh/"$@" ; }

# CLI weather forecast
function weather() { curl wttr.in/"$@" ; curl v2.wttr.in/"$@" ; }


# timestamp things
alias timestamp="date +%Y%m%d-%H%M%S"
alias logtimestamp='echo "<<<<<" $(date +%Y%m%d-%H%M%S) ">>>>>"'

# file things
alias removedones="find . -name \*.done -exec rm {} \;"
alias cleanmail='sqlite3 ~/Library/Mail/Envelope\ Index vacuum;'
alias changed_today='find ~ -type f -mtime 0'

# Linux package management
if [[ "z${DISTRO}" == "zCentos" ]]; then
    alias list-packages='yum list installed'
    alias remove-package-fully='sudo yum remove $@' # As close as you'll get
elif [[ "z${DISTRO}" == "zUbuntu" ]]; then
    alias list-packages='dpkg --get-selections | grep -v deinstall'
    alias remove-package-fully='sudo apt-get --purge remove $@'
fi

# Mac things
if [[ "z${PLATFORM}" == "zOSX" ]]; then
    alias macvim='/Applications/MacVim.app/Contents/MacOS/Vim -g'
    alias minecraft_server='java -Xmx1024M -Xms1024M -jar ~/Downloads/minecraft_server.jar nogui'
    # VirtualBox things
    alias listvms='/Applications/VirtualBox.app/Contents/MacOS/VBoxManage list vms'
    alias startweb='VBoxManage startvm --type headless michaeldavies.org'
fi

# Python things
alias pydoc='python -m pydoc'
alias pycheck="python -m py_compile $@"
alias tox="check-status.sh \tox $@"
alias jsondecode='python -mjson.tool'
#export PIP_REQUIRE_VIRTUALENV=true    # Ensure pip only runs in virtualenvs

# XML things
alias xmldecode='python -c "import sys, xml.dom.minidom; print xml.dom.minidom.parseString(sys.stdin.read()).toprettyxml()"'

# Java things
#export JAVA_HOME=${HOME}/src/java

# Ansible things
export ANSIBLE_NOCOWS=1

# Paranoid things :)
alias whoislistening='for IP in $(netstat -an | grep tcp | cut -c45- | grep -v \* | cut -f1 -d" " | cut -f1,2,3,4 -d\. | sort | uniq); do echo -n $IP; whois $IP | grep OrgName | cut -c16-; done'

# Virtualenvwrapper
if test -x /usr/local/bin/virtualenvwrapper.sh; then
    # Standard python installation location
    . /usr/local/bin/virtualenvwrapper.sh
elif test -x /etc/bash_completion.d/virtualenvwrapper; then
    # Ubuntu borkedness
    . /usr/local/bin/virtualenvwrapper.sh
fi

# Bash completion in interactive shells
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
      . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
      . /etc/bash_completion
  else
    if __command_exists brew; then
        if [ -f $(brew --prefix)/etc/bash_completion ]; then
            . $(brew --prefix)/etc/bash_completion
        fi
    fi
  fi
fi

# Git things
alias gitbackup="git status --porcelain | cut -d' ' -f 3 | xargs backup.sh"
alias gitcleanup="git status --porcelain | cut -f 2 -d ' ' | xargs rm -rf"
#export GIT_EXTERNAL_DIFF=git-diff-using-sdiff.sh

# Set up path correctly
export PATH=${HOME}/bin/noarch:/usr/local/bin:${HOME}/bin/`arch`/`uname`:${PATH}:${JAVA_HOME}/bin:${GOROOT}/bin:${HOME}/apps/PhpStorm/bin:${HOME}/apps/freeplane/freeplane:${HOME}/apps/intelliJ/idea/bin:${HOME}/apps/packer

# Go things
export GOROOT=${HOME}/src/go
export GOPATH=${HOME}/src/gocode

# Perl things
function profile-perl()
{
    echo "Profiling $1"
    time perl -d:NYTProf $1
    nytprofhtml nytprof.out
    open nytprof/index.html
}

# Ansible things (not anymore)
#export ANSIBLE_CONFIG=${HOME}/.ansible.cfg

# Misc things
alias plusone="figlet '+1' | cowsay -n | sed -e 's/^/  /'"

# ssh agent stuff
#mkdir -p "$HOME/etc/ssh"
#
#function short-hostname {
#    printf $(hostname | cut -f1 -d'.')
#}

#function start-ssh-agent {
#    eval `ssh-agent -s -a ${HOME}/etc/ssh/ssh-agent-socket`;
#    ssh-add ${HOME}/.ssh/id_rsa
#}
#
#if [ ${SSH_AGENT_PID} ]; then
#    RUNNING="$(ps ${SSH_AGENT_PID} | grep ssh-agent-socket)"
#    if [ -z "${RUNNING}" ]; then
#        start-ssh-agent
#    fi
#fi

# Micropython things
#export AMPY_PORT=/dev/tty.SLAB_USBtoUART


#
# Prompt mangling
#

# Are we in a screen session?
__screen_ps1 ()
{
    if [ -n "${STY}" ]; then
        printf "(${STY})"
    fi
}

# Git me harder!
__git_ps1 ()
{
    local g="$(git rev-parse --git-dir 2>/dev/null)"
    if [ -n "$g" ]; then
        local r
        local b
        if [ -d "$g/../.dotest" ]
        then
            local b="$(git symbolic-ref HEAD 2>/dev/null)"
            r="|REBASING"
        elif [ -d "$g/.dotest-merge" ]
        then
            r="|REBASING"
            b="$(cat $g/.dotest-merge/head-name)"
        elif [ -f "$g/MERGE_HEAD" ]
        then
            r="|MERGING"
            b="$(git symbolic-ref HEAD 2>/dev/null)"
        else
            if [ -f $g/BISECT_LOG ]
            then
                r="|BISECTING"
            fi
            if ! b="$(git symbolic-ref HEAD 2>/dev/null)"
            then
                b="$(cut -c1-7 $g/HEAD)..."
            fi
        fi
        if [ -n "$1" ]; then
            printf "$1" "${b##refs/heads/}$r"
        else
            printf " (%s)" "${b##refs/heads/}$r"
        fi
    fi
}

export PS1="${PS1//\\w/\\w\$(__git_ps1)$(__screen_ps1)}"

# Red Hat has decided to start quoting files/dirs with spaces.
# Let's change the behaviour back to normal.
alias ls='/usr/bin/ls --quoting-style=literal -F --color=auto'

# ls by size and time
alias lss='ls --human-readable --size -1 -S --classify'
alias lst='ls -t -l'

# Only show drives and not all the other guff
alias mnt="mount | awk -F' ' '{ printf \"%s\t%s\n\",\$1,\$3; }' | column -t | egrep ^/dev/ | sort"

# Find things in my history
alias gh='history|grep'

# Auto-tmux ssh
function tssh ()
{
    if [[ ! -z $1 ]] && [[ $1 != 'localhost' ]]; then
        ssh -t $1 'tmux a || tmux'
    fi
}

function tm ()
{
    if [[ ! -z $1 ]] && [[ $1 != 'localhost' ]]; then
        tmux a -t $1 || tmux new $1
    else
        tmux a || tmux new
    fi
}

# Blink-tool
function _b ()
{
    if hash blink1-tool &> /dev/null; then
        hash blink1-tool && blink1-tool $1 >/dev/null 2>&1
    fi
}
alias boff="_b --off"

# Protect my work machine from devstack
touch $HOME/.no-devstack

# Brewery API test key
#export BDB_API_KEY="d28a194879ac624eb01e41050ca412e5"

# X1 Carbon projector fixes for Centos 7
#function fix-screens {
#    xrandr --output DP-2-2 --off
#    xrandr --output DP-2-2 --right-of eDP-1 --auto
#    xrandr --output DP-2-1 --off
#    xrandr --output DP-2-1 --right-of DP-2-2 --auto
#}
#
#function fix-HDMI-1080 {
#    xrandr --output HDMI1 --mode 1920x1080
#}

# Anything after here was probably automagically added,
# and should be re-categorised

