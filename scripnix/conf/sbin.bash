# Root-user utility script definitions. All root-user scripts source this file.

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

scriproot=$(whereis-scripnix)
source "${scriproot}/conf/bin.bash"

# Set configuration variables, overriding as necessary.
sconf_file='sconf.bash'
source "${scriproot}/conf/${sconf_file}"
[[ -r "${SYSTEM_CONF_DIR}/${sconf_file}" ]] && source "${SYSTEM_CONF_DIR}/${sconf_file}"
