# Command alias definitions. Do not edit these. Instead, override values as needed in /etc/scripnix/conf.bash or ~/.scripnix/conf.bash.

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'

# TODO: automate substitution of GNU commands on MacOS
if [[ $(os-name) == 'macos' ]]; then
    alias l='gls -v --color=tty'
    alias ls='gls -v --color=tty'
    alias ll='gls -lv --color=tty --time-style=long-iso'
    alias la='gls -lv --almost-all --color=tty --time-style=long-iso'
    alias lh='gls -lv --human-readable --color=tty --time-style=long-iso'
    alias lm='gls -lv --block-size=1024K --color=tty --time-style=long-iso'
    alias lt='gls -lt --color=tty --time-style=long-iso'
    alias lrt='gls -lrt --color=tty --time-style=long-iso'
else
    alias l='ls -v --color=tty'
    alias ls='ls -v --color=tty'
    alias ll='ls -lv --color=tty --time-style=long-iso'
    alias la='ls -lv --almost-all --color=tty --time-style=long-iso'
    alias lh='ls -lv --human-readable --color=tty --time-style=long-iso'
    alias lm='ls -lv --block-size=1024K --color=tty --time-style=long-iso'
    alias lt='ls -lt --color=tty --time-style=long-iso'
    alias lrt='ls -lrt --color=tty --time-style=long-iso'
fi

alias ltt='last -a | tac | tail -n20'

[[ $(os-name) == 'macos' ]] || alias nst='netstat --all --numeric --tcp --udp'
[[ $(os-name) == 'macos' ]] && alias nst='netstat -anv -finet'

hash iftop >/dev/null 2>&1 && alias ift='sudo iftop -nNPB'
hash iptables >/dev/null 2>&1 && alias ipt='sudo iptables -nvL'

[[ $(os-name) == 'macos' ]] || alias pe='ps -eFlT'
alias px='ps aux'

# Necessary to enable aliases in shell scripts.
shopt -s expand_aliases
