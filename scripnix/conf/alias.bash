# Command alias definitions. Do not edit these. Instead, override values as needed in /etc/scripnix/conf.bash or ~/.scripnix/conf.bash.

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'

gls=$(gnu_equivalent 'ls')
alias l="${gls} -v --color=tty"
alias ls="${gls} -v --color=tty"
alias ll="${gls} -lv --color=tty --time-style=long-iso"
alias la="${gls} -lv --almost-all --color=tty --time-style=long-iso"
alias lh="${gls} -lv --human-readable --color=tty --time-style=long-iso"
alias lm="${gls} -lv --block-size=1024K --color=tty --time-style=long-iso"
alias lt="${gls} -lt --color=tty --time-style=long-iso"
alias lrt="${gls} -lrt --color=tty --time-style=long-iso"

alias dim="echo $(tput cols)x$(tput lines)"

is_macos="false"
[[ $(os-name) == 'macos' ]] && is_macos="true"

gtac=$(gnu_equivalent 'tac')
${is_macos} || alias ltt="last -a | ${gtac} | tail -n20"
${is_macos} && alias ltt="last | ${gtac} | tail -n20"

${is_macos} || alias nst='netstat --all --numeric --tcp --udp'
${is_macos} && alias nst='netstat -anv -finet'

hash iftop >/dev/null 2>&1 && alias ift='sudo iftop -nNPB'
hash iptables >/dev/null 2>&1 && alias ipt='sudo iptables -nvL'

${is_macos} || alias pe='ps -eFlT'
alias px='ps aux'

hash git >/dev/null 2>&1 && alias gl='git log -40 --all --decorate --graph --oneline'
hash git >/dev/null 2>&1 && alias gs='git status'

alias sudo='sudo '
