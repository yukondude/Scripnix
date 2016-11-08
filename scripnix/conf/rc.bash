# Interactive shell configuration. ~/.bashrc or ~/.profile should source this file.

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

scriproot="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

source "${scriproot}/conf/bin.bash"

if [[ $(id -u) -eq 0 ]] ; then
    source "${scriproot}/conf/sbin.bash"
fi

# Don't logout after Ctrl+D.
set -o ignoreeof

# Colourful prompt.
if [[ $(id -u) -eq 0 ]] ; then
    user_colour='\[\033[01;31m\]'
    user_prompt='#'
else
    user_colour='\[\033[01;32m\]'
    user_prompt='\$'
fi

host_name=$(hostname -s | tr '[:upper:]' '[:lower:]')

# TODO: Capitalize the host name for remote connections.
#if [[ is-remote-cnx ]]; then
#    host_name=$(hostname -s | tr '[:lower:]' '[:upper:]')
#fi

base_colour='\[\033[00m\]'
alt_colour='\[\033[01;34m\]'

export PS1="${user_colour}\u${alt_colour}@${host_name} ${user_colour}\D{%H:%M:%S} ${alt_colour}\w ${user_colour}${user_prompt}${base_colour} "
