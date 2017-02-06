# Command alias definitions. Do not edit these. Instead, override values as needed in /etc/scripnix/conf.bash or ~/.scripnix/conf.bash.

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'

ls_equivalent=$(gnu_equivalent 'ls')
alias l="${ls_equivalent} -v --color=tty"
alias ls="${ls_equivalent} -v --color=tty"
alias ll="${ls_equivalent} -lv --color=tty --time-style=long-iso"
alias la="${ls_equivalent} -lv --almost-all --color=tty --time-style=long-iso"
alias lh="${ls_equivalent} -lv --human-readable --color=tty --time-style=long-iso"
alias lm="${ls_equivalent} -lv --block-size=1024K --color=tty --time-style=long-iso"
alias lt="${ls_equivalent} -lt --color=tty --time-style=long-iso"
alias lrt="${ls_equivalent} -lrt --color=tty --time-style=long-iso"

alias dim="echo $(tput cols)x$(tput lines)"

alias degrep='egrep --invert-match'
alias degrep-rcs="degrep '\/(\.hg|\.git|\.svn)'"

is_macos="false"
[[ $(os-name) == 'macos' ]] && is_macos="true"

tac_equivalent=$(gnu_equivalent 'tac')
${is_macos} || alias ltt="last -a | ${tac_equivalent} | tail -n20"
${is_macos} && alias ltt="last | ${tac_equivalent} | tail -n20"

${is_macos} || alias nst='netstat --all --numeric --tcp --udp'
${is_macos} && alias nst='netstat -anv -finet'

hash iftop >/dev/null 2>&1 && alias ift='sudo iftop -nNPB'
hash iptables >/dev/null 2>&1 && alias ipt='sudo iptables -nvL'

${is_macos} || alias pe='ps -eFlT'
alias px='ps aux'

hash git >/dev/null 2>&1 && alias gl='git log -40 --all --decorate --graph --oneline'
hash git >/dev/null 2>&1 && alias gs='git status'

alias sudo='sudo '

# Necessary to enable aliases in shell scripts.
shopt -s expand_aliases
