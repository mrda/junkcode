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

