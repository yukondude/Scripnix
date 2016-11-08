# Configuration variables. Do not edit these. Instead, override values as needed in /etc/scripnix/conf.bash or ~/.scripnix/conf.bash.
#
# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

# Configuration setting directories (once Scripnix is installed).
SYSTEM_CONF_DIR='/etc/scripnix'
USER_CONF_DIR="${HOME}/.scripnix"

# Temporary directory (to which pretty much every user has write permissions).
TMP_DIR='/tmp'

# Exclusions from find searches.
FIND_PATH_EXCLUDE='( -path /dev -or -path /proc -or -path /sys ) -prune'
