# Root-user configuration variables. Do not edit these. Instead, override values as needed in /etc/scripnix/sconf.bash or
# ~/.scripnix/sconf.bash.
#
# This file is part of Scripnix. Copyright 2016 Dave Rogers <info@yukondude.com>. Licensed under the GNU General Public License, version 3.
# Refer to the attached LICENSE file or see <http://www.gnu.org/licenses/> for details.

ARCHIVE_DIR='/var/archive'
ARCHIVE_EXCLUSIONS='/etc/scripnix/archive-exclusions'
ARCHIVE_PATHS_DIR='/etc/scripnix/archive-paths'

MYSQL_DB_DIR='/var/lib/mysql'
MYSQL_DUMP_FILE='mysql-dump.tar'

PGSQL_DUMP_FILE='pgsql-dump.tar'

SYSTEM_CRONTAB='/etc/crontab'
SYSTEM_CRON_DIR='/etc/cron.d'
