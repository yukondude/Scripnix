# Interactive shell configuration. ~/.bashrc or ~/.profile should source this file.

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

scriproot=$(whereis-scripnix)
source "${scriproot}/conf/bin.bash"
source "${scriproot}/conf/alias.bash"

if [[ $(id -u) -eq 0 ]] ; then
    source "${scriproot}/conf/sbin.bash"
    source "${scriproot}/conf/salias.bash"
fi

# Don't logout after Ctrl+D.
set -o ignoreeof

# Colourful prompt.
base_colour='\[\033[00m\]'
alt_colour='\[\033[01;34m\]'
remote_colour='\[\033[01;33m\]'

if [[ $(id -u) -eq 0 ]] ; then
    user_colour='\[\033[01;31m\]'
    user_prompt='#'
else
    user_colour='\[\033[01;32m\]'
    user_prompt='\$'
fi

host_name=$(hostname -s | tr '[:upper:]' '[:lower:]')

if is-remote-cnx ; then
    host_name="${remote_colour}${host_name}"
fi

export PS1="${user_colour}\u${alt_colour}@${host_name} ${user_colour}\D{%H:%M:%S} ${alt_colour}\w ${user_colour}${user_prompt}${base_colour} "
