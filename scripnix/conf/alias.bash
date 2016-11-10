# Command alias definitions. Do not edit these. Instead, override values as needed in /etc/scripnix/conf.bash or ~/.scripnix/conf.bash.

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'

alias l="$(gnu_equivalent 'ls') -v --color=tty"
alias ls="$(gnu_equivalent 'ls') -v --color=tty"
alias ll="$(gnu_equivalent 'ls') -lv --color=tty --time-style=long-iso"
alias la="$(gnu_equivalent 'ls') -lv --almost-all --color=tty --time-style=long-iso"
alias lh="$(gnu_equivalent 'ls') -lv --human-readable --color=tty --time-style=long-iso"
alias lm="$(gnu_equivalent 'ls') -lv --block-size=1024K --color=tty --time-style=long-iso"
alias lt="$(gnu_equivalent 'ls') -lt --color=tty --time-style=long-iso"
alias lrt="$(gnu_equivalent 'ls') -lrt --color=tty --time-style=long-iso"

[[ $(os-name) == 'macos' ]] || alias ltt="last -a | $(gnu_equivalent 'tac') | tail -n20"
[[ $(os-name) == 'macos' ]] && alias ltt="last | $(gnu_equivalent 'tac') | tail -n20"

[[ $(os-name) == 'macos' ]] || alias nst='netstat --all --numeric --tcp --udp'
[[ $(os-name) == 'macos' ]] && alias nst='netstat -anv -finet'

hash iftop >/dev/null 2>&1 && alias ift='sudo iftop -nNPB'
hash iptables >/dev/null 2>&1 && alias ipt='sudo iptables -nvL'

[[ $(os-name) == 'macos' ]] || alias pe='ps -eFlT'
alias px='ps aux'

alias sudo='sudo '

# Necessary to enable aliases in shell scripts.
shopt -s expand_aliases
