# Michael's aliases :-)
alias l="ls -la $@"  # args quoted
alias cls="clear"
alias tstamp="date +%Y%m%d-%H%M%S"
alias timestamp="date +%Y%m%d-%H%M%S"
alias removedones="find . -name \*.done -exec rm {} \;"
alias tac="perl -e 'print reverse <> '"
alias freq_commands="history|awk '{a[$2]++} END{for(i in a){printf \"%5d\t%s \n\",a[i],i}}'|sort -rn|head"
alias cleanmail='sqlite3 ~/Library/Mail/Envelope\ Index vacuum;'
alias changed_today='find ~ -type f -mtime 0'
alias macvim='/Applications/MacVim.app/Contents/MacOS/Vim -g'
alias list-packages='dpkg --get-selections | grep -v deinstall'
alias remove-package-fully='sudo apt-get --purge remove $@'

# I loves my pips
if [ ! -d ${HOME}/.pipcache ]; then
    # Control will enter here if $DIRECTORY doesn't exist.
    mkdir ${HOME}/.pipcache
fi
export PIP_DOWNLOAD_CACHE=${HOME}/.pipcache

# Set up path correctly
export PATH=${HOME}/bin/noarch:${HOME}/bin/`arch`/`uname`:${PATH}

# Handy functions
function profile-perl()
{
echo "Profiling $1"
time perl -d:NYTProf $1
nytprofhtml nytprof.out
open nytprof/index.html
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

# ssh agent
if test -x /usr/bin/ssh-agent; then
    sock=`netstat -l 2>/dev/null|grep ssh-|cut -c 58-|head -n 1`
    if test -n "$sock"; then
            export SSH_AUTH_SOCK=$sock
    else
            eval `ssh-agent`
    fi
fi

# virtualenvwrapper
if test -x /usr/local/bin/virtualenvwrapper.sh; then
    # Standard python installation location
    source /usr/local/bin/virtualenvwrapper.sh
elif test -x /etc/bash_completion.d/virtualenvwrapper; then
    # Ubuntu borkedness
    source /usr/local/bin/virtualenvwrapper.sh
fi

export EDITOR=vim
export VISUAL=vim
export PS1="${PS1//\\w/\\w\$(__git_ps1)}"
export LESS="-R" # so we get colour
export LESSOPEN='|~/.lessfilter %s'
export ACK_OPTIONS="--color" # so we get color

alias pycheck="python -m py_compile $@"
alias tox="check-status.sh /usr/local/bin/tox $@"
alias gitbackup="git status --porcelain | cut -d' ' -f 3 | xargs backup.sh"
alias gitcleanup="git status --porcelain | cut -f 2 -d ' ' | xargs rm -rf"
alias re-auth="eval `ssh-agent -s`"
alias jsondecode='python -mjson.tool'
alias standup='speechinator.py mikal mrda jhesketh loquacities mattoliverau asettle neillc Darren JRobinson gus'

