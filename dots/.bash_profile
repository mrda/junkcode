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

# ssh complete. A bastardised version of http://superuser.com/questions/52483?tab=votes&page=2#answer-167562 .
#complete -o default -o nospace -W "$(/usr/bin/env ruby -ne 'puts $_.split(/[,\s]+/)[1..-1].reject{|host| host.match(/\*|\?/)} if $_.match(/^\s*Host\s+/);' < $HOME/.ssh/config)" sc
complete -o default -o nospace -W "$(perl -p -i -e 's/([^\s0-9]*)(,|\s).*/\1/' < ~/.ssh/known_hosts | grep '^[a-z]' | sort)" scp sftp ssh sr

export EDITOR=vim
export VISUAL=vim
export PATH=$HOME/bin:$HOME/src/projects/junkcode:$PATH

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

export PS1="${PS1//\\w/\\w\$(__git_ps1)}"
export LESS="-R" # so we get colour
export ACK_OPTIONS="--color" # so we get color


