# Common utility script definitions. All scripts should source this file.

# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

scriproot=$(whereis-scripnix)
source "${scriproot}/conf/func.bash"

# Set configuration variables, overriding as necessary.
conf_file='conf.bash'
source "${scriproot}/conf/${conf_file}"
[[ -r "${SYSTEM_CONF_DIR}/${conf_file}" ]] && source "${SYSTEM_CONF_DIR}/${conf_file}"
[[ -r "${USER_CONF_DIR}/${conf_file}" ]] && source "${USER_CONF_DIR}/${conf_file}"
