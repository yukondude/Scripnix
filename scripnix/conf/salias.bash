# Root-user command alias definitions. Do not edit these. Instead, override values as needed in /etc/scripnix/sconf.bash or
# ~/.scripnix/sconf.bash.

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

hash iftop >/dev/null 2>&1 && alias ift='iftop -nNPB'

hash iptables >/dev/null 2>&1 && alias ipt='iptables -nvL'

is_macos="false"
[[ $(os-name) == 'macos' ]] && is_macos="true"

${is_macos} || alias nst='netstat --all --numeric --program --tcp --udp'
${is_macos} && alias nst='netstat -an -finet -v'
